import os
import re
import subprocess
from multiprocessing import Process
from threading import Timer
from typing import List, Tuple, Union

# TODO: fix template to within their own folder, kinda of like a dump folder for user
from FuzzAll.target.QISKIT.template import qiskit_parameter
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL


class QiskitTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a Qiskit Fuzzer"
        if kwargs["template"] == "qiskit_parameter":
            self.prompt_used = qiskit_parameter
        else:
            raise NotImplementedError

    def write_back_file(self, code):
        try:
            with open(f"/tmp/temp{self.CURRENT_TIME}.py", "w", encoding="utf-8") as f:
                f.write(code)
        except Exception:
            pass
        return f"/tmp/temp{self.CURRENT_TIME}.py"

    def wrap_prompt(self, prompt: str) -> str:
        return f"/* {prompt} */\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f'""" {prompt} """'

    def filter(self, code) -> bool:
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        if self.prompt_used["target_api"] not in clean_code:
            return False
        return True

    def clean(self, code: str) -> str:
        code = self._comment_remover(code)
        return code

    def clean_code(self, code: str) -> str:
        """Remove all comments and empty lines from a string of Python code."""
        code = self._comment_remover(code)
        code = "\n".join(
            [
                line
                for line in code.split("\n")
                if line.strip() != "" and line.strip() != self.prompt_used["begin"]
            ]
        )
        return code

    def _comment_remover(self, code: str) -> str:
        """Remove all comments from a string of Python code."""
        # Remove inline comments
        code = re.sub(r"#.*", "", code)
        # Remove block comments
        code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)
        return code

    def _validate_static(self, filename) -> Tuple[FResult, str]:
        """Validate the input at the filename path statically (no execution).

        Typically, this is done by checking the return code of the compiler.
        For dynamically typed languages, we could perform both a parser and
        static analysis on the code.
        """

        def parsing_routine(filename: str):
            import ast

            content = open(filename, "r", encoding="utf-8").read()
            ast.parse(content)

        # run the parsing routine with a timeout
        p = Process(target=parsing_routine, args=(filename,))
        p.start()
        p.join(timeout=5)

        if p.is_alive():
            # kill the process
            p.terminate()
            return FResult.ERROR, "parsing timed out"

        exit_code = p.exitcode
        if exit_code != 0:
            return FResult.ERROR, "parsing failed"

        return FResult.SAFE, "its safe"

    def _kill_program(self, filename: str) -> None:
        """Kill a program running at the filename path."""
        pname = f"'{filename}'"
        subprocess.run(
            ["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"],
            shell=True,
        )
        subprocess.run(
            [
                "ps -ef | grep "
                + pname
                + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"
            ],
            shell=True,
        )  # kill all tests thank you

    def validate_individual(self, filename) -> Tuple[FResult, str]:
        """Apply the oracle to define whether the input is valid or not.

        A possible oracle could be to run the same programs with two different
        compilation levels. If the outputs are the same, then the program is
        valid. If one of the two crashes, then there is a problem (crash
        oracle).
        """

        # ORACLE: two optimization levels
        # 0: no optimization
        # 3: full optimization
        OPT_LEVELS = [0, 3]

        program_content = open(filename, "r", encoding="utf-8").read()

        # if not ending with \n then delete the last line
        content = open(filename, "r", encoding="utf-8").read()
        if not content.endswith("\n"):
            lines = content.split("\n")
            lines = lines[:-1]
            content = "\n".join(lines)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        program_content = content

        # fake execution
        self.v_logger.logo(f"python {filename}:")
        self.v_logger.logo("\n" + program_content)
        self.v_logger.logo("-" * 20)

        # check if it can be parsed
        parser_result, parser_msg = self._validate_static(filename)
        if parser_result != FResult.SAFE:
            return parser_result, parser_msg

        # check that it contains a circuit " qc."
        if "qc." not in program_content:
            return FResult.ERROR, "no circuit `qc.` found"

        # check that the code can be transpiled
        # create two variants of the programs with different opt. levels
        # run the two programs with a timeout
        # if one of them times out, then we return an error
        exit_codes = {}
        for opt_level in OPT_LEVELS:
            exit_codes[opt_level] = None
            # store the program in a temporary file
            new_filename = f"/tmp/temp{self.CURRENT_TIME}_lvl_{opt_level}.py"
            only_new_filename = os.path.basename(new_filename)
            i_content = program_content
            i_content += "\nfrom qiskit.compiler import transpile"
            i_content += f"\nqc = transpile(qc, optimization_level={opt_level})"
            with open(new_filename, "w", encoding="utf-8") as f:
                f.write(i_content)
                f.close()
            try:
                # cmd = f"echo {new_filename}"
                # cmd = f"python {new_filename}"
                # docker run -v {new_filename}:/{only_new_filename} qiskit-driver {only_new_filename}
                cmd = f"docker run -v {new_filename}:/{only_new_filename} qiskit-driver {only_new_filename}"
                exit_code = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    encoding="utf-8",
                    timeout=15,
                    text=True,
                )
                exit_codes[opt_level] = exit_code
                self.v_logger.logo(f"Execution result: {exit_code}")
            except ValueError as e:
                self._kill_program(filename)
                return FResult.ERROR, f"ValueError: {str(e)}"
            except subprocess.TimeoutExpired:
                # kill program
                self._kill_program(filename)
                return FResult.TIMED_OUT, f"timed out for opt level {str(opt_level)}"

        for opt_level in OPT_LEVELS:
            if exit_codes[opt_level] is None:
                return (
                    FResult.ERROR,
                    f"no exit code found for opt level {str(opt_level)}",
                )

        # raise an error if the two programs have different outputs
        if exit_codes[0].stdout != exit_codes[3].stdout:
            return FResult.ERROR, "different outputs"

        # if the two programs have the same output, then we return SAFE
        return FResult.SAFE, "its safe"
