import ast
import os
import re
import subprocess
from enum import Enum
from multiprocessing import Process
from threading import Timer
from typing import List, Tuple, Union

# TODO: fix template to within their own folder, kinda of like a dump folder for user
from FuzzAll.target.QISKIT.template import (
    qiskit_basic,
    qiskit_hw_qasm,
    qiskit_hw_transpile,
    qiskit_parameter,
)
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL

# create an enum with some code snippets


class Snippet(Enum):
    READ_ANY_QASM_SAME_FOLDER = """
from qiskit import QuantumCircuit
import glob

qasm_files = glob.glob("*.qasm")
for qasm_file in qasm_files:
    print(f"Importing {qasm_file}")
    try:
        qc = QuantumCircuit.from_qasm_file(qasm_file)
    except Exception as e:
        print(f"Exception: {e}")
        print(f"File: {qasm_file}")
        content = open(qasm_file, "r").read()
        print(f"Content: {content}")
    """
    TRANSPILE_QC_OPT_LVL_0 = """
from qiskit.compiler import transpile
qc = transpile(qc, optimization_level=0)
"""
    TRANSPILE_QC_OPT_LVL_1 = """
from qiskit.compiler import transpile
qc = transpile(qc, optimization_level=1)
"""
    TRANSPILE_QC_OPT_LVL_2 = """
from qiskit.compiler import transpile
qc = transpile(qc, optimization_level=2)
"""
    TRANSPILE_QC_OPT_LVL_3 = """
from qiskit.compiler import transpile
qc = transpile(qc, optimization_level=3)
"""


class QiskitTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a Qiskit Fuzzer"
        if kwargs["template"] == "fuzzing_with_config_file":
            config_dict = kwargs["config_dict"]
            self.prompt_used = self._create_prompt_from_config(config_dict)
            self.config_dict = config_dict
        elif kwargs["template"] == "qiskit_parameter":
            self.prompt_used = qiskit_parameter
        elif kwargs["template"] == "qiskit_basic":
            self.prompt_used = qiskit_basic
        elif kwargs["template"] == "qiskit_hw_qasm":
            self.prompt_used = qiskit_hw_qasm
        elif kwargs["template"] == "qiskit_hw_transpile":
            self.prompt_used = qiskit_hw_transpile
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

        try:
            content = open(filename, "r", encoding="utf-8").read()
            ast.parse(content)
        except Exception as e:
            return FResult.LLM_WEAKNESS, f"parsing failed {e}"

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

    def _remove_partial_lines(self, content: str) -> None:
        """Remove the last line if it is not ending with new line."""
        if not content.endswith("\n"):
            lines = content.split("\n")
            lines = lines[:-1]
            content = "\n".join(lines)
        return content

    def _delete_last_line_inplace(self, filename: str) -> None:
        """Delete the last line of a file."""
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        lines = lines[:-1]
        content = "\n".join(lines)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def validate_individual(self, filepath: str) -> Tuple[FResult, str]:
        """Apply the oracle to define whether the input is valid or not."""

        # check if it can be parsed
        parser_result, parser_msg = self._validate_static(filepath)
        if parser_result != FResult.SAFE:
            # try to recover from the parser error by removing the last line
            self._delete_last_line_inplace(filepath)
            # try to parse again
            parser_result, parser_msg = self._validate_static(filepath)
            if parser_result != FResult.SAFE:
                return parser_result, parser_msg

        # check if the config_dict attribute exists
        if hasattr(self, "config_dict"):
            target = self.config_dict["target"]
            oracle = target["oracle"]
            if oracle == "crash":
                return self._validate_with_crash_oracle(filepath)
            elif oracle == "diff":
                return self._validate_with_diff_opt_levels(filepath)
            elif oracle == "metamorphic":
                return self._validate_with_QASM_roundtrip(filepath)

        return self._validate_with_crash_oracle(filepath)

    def _validate_with_diff_opt_levels(self, filepath: str) -> Tuple[FResult, str]:
        """Validate the input with different optimization levels.

        It runs the same programs with two different
        compilation levels. If the outputs are the same, then the program is
        valid. If one of the two crashes, then there is a problem (crash
        oracle).
        """

        # ORACLE: two optimization levels
        # 0: no optimization
        # 3: full optimization
        OPT_LEVELS_SNIPPETS = [
            Snippet.TRANSPILE_QC_OPT_LVL_0,
            Snippet.TRANSPILE_QC_OPT_LVL_3,
        ]

        program_content = open(filepath, "r", encoding="utf-8").read()

        # fake execution
        self.v_logger.logo(f"python {filepath}:")
        self.v_logger.logo("\n" + program_content)
        self.v_logger.logo("-" * 20)

        # check that it contains a circuit " qc."
        if "qc." not in program_content:
            return FResult.FAILURE, "no circuit `qc.` found"

        # check that the code can be transpiled
        # create two variants of the programs with different opt. levels
        # run the two programs with a timeout
        # if one of them times out, then we return an error
        exit_codes = {}
        for lvl, opt_level_snippet in zip([0, 3], OPT_LEVELS_SNIPPETS):
            exit_codes[opt_level_snippet] = None
            # store the program in a temporary file
            new_filename = f"/tmp/temp{self.CURRENT_TIME}_lvl_{lvl}.py"
            only_new_filename = os.path.basename(new_filename)
            i_content = program_content + "\n" + str(opt_level_snippet.value)
            with open(new_filename, "w", encoding="utf-8") as f:
                f.write(i_content)
                f.close()
            try:
                # cmd = f"echo {new_filename}"
                # cmd = f"python {new_filename}"
                # docker run -v {new_filename}:/{only_new_filename} qiskit-driver {only_new_filename}
                cmd = f"docker run --rm -v {new_filename}:/{only_new_filename} qiskit-driver {only_new_filename}"
                exit_code = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    encoding="utf-8",
                    timeout=15,
                    text=True,
                )
                exit_codes[opt_level_snippet] = exit_code
                self.v_logger.logo(f"Execution result: {exit_code}")
            except ValueError as e:
                self._kill_program(filepath)
                return FResult.FAILURE, f"ValueError: {str(e)}"
            except subprocess.TimeoutExpired:
                # kill program
                self._kill_program(filepath)
                return FResult.TIMED_OUT, f"timed out for opt level {str(lvl)}"

        for opt_level in OPT_LEVELS_SNIPPETS:
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

    def _validate_with_crash_oracle(self, filepath: str) -> Tuple[FResult, str]:
        """Check wether the transpiler returns an exception or not.

        If the exception is a TranspilerError, then the program is valid and
        the bug is in the transpiler. If the exception is another one, then
        the program is invalid.
        """
        abs_path = os.path.abspath(filepath)
        only_filename = os.path.basename(filepath)
        try:
            cmd = f"docker run --rm -v {abs_path}:/{only_filename} qiskit-driver {only_filename}"
            exit_code = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=5,
                text=True,
            )
            self.v_logger.logo(f"Execution result: {exit_code}")
            if exit_code.returncode == 0:
                return FResult.SAFE, "its safe"
            else:
                # check if the output contained a TranspilerError
                if "TranspilerError" in exit_code.stderr:
                    return FResult.ERROR, exit_code.stderr
                else:
                    return FResult.FAILURE, "its safe"
        except ValueError as e:
            self._kill_program(filepath)
            return FResult.FAILURE, f"ValueError: {str(e)}"
        except subprocess.TimeoutExpired:
            # kill program
            self._kill_program(filepath)
            return FResult.TIMED_OUT, f"timed out"

    def _validate_with_QASM_roundtrip(self, filepath: str) -> Tuple[FResult, str]:
        """Check if the exported qasm (if any) can be parsed by the QASM parser."""
        # append the snippet to read the qasm files
        program_content = open(filepath, "r", encoding="utf-8").read()
        program_content += "\n" + str(Snippet.READ_ANY_QASM_SAME_FOLDER.value)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(program_content)
            f.close()
        abs_path = os.path.abspath(filepath)
        only_filename = os.path.basename(filepath)
        try:
            cmd = f"docker run --rm -v {abs_path}:/{only_filename} qiskit-driver {only_filename}"
            exit_code = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=5,
                text=True,
            )
            self.v_logger.logo(f"Execution result: {exit_code}")
            if exit_code.returncode == 0:
                return FResult.SAFE, "its safe"
            else:
                # check if the output contained a QasmError
                if "QasmError" in exit_code.stderr:
                    return FResult.ERROR, "qasm error: POTENTIAL BUG"
                else:
                    return FResult.FAILURE, exit_code.stderr
        except ValueError as e:
            self._kill_program(filepath)
            return FResult.FAILURE, f"ValueError: {str(e)}"
        except subprocess.TimeoutExpired:
            # kill program
            self._kill_program(filepath)
            return FResult.TIMED_OUT, f"timed out"
