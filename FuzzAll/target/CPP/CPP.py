import re
import subprocess
import time
from typing import List, Union

import torch

# TODO: fix template to within their own folder, kinda of like a dump folder for user
from FuzzAll.target.CPP.template import (
    cpp_23,
    cpp_apply,
    cpp_expected,
    cpp_expected_example,
    cpp_is_scoped_enum,
    cpp_optional,
    cpp_span,
    cpp_variant,
)
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL
from FuzzAll.util.util import comment_remover

main_code = """
int main(){
return 0;
}
"""


def get_gcc_supported_standard() -> List[str]:
    """Returns the list of all the GCC standards supported by the system.

    This replicates the equivalent bash command:
    gcc -v --help 2> /dev/null | sed -n '/^ *-std=\([^<][^ ]\+\).*/ {s//\1/p}'
    """
    gcc_help = subprocess.run(
        "gcc -v --help 2> /dev/null", shell=True, capture_output=True
    )
    gcc_help = gcc_help.stdout.decode("utf-8")
    gcc_help = gcc_help.split("\n")
    gcc_help = [line.strip() for line in gcc_help]
    gcc_help = [line for line in gcc_help if line.startswith("-std=")]
    gcc_help = [line.split("=")[1] for line in gcc_help]
    gcc_help = [line.split(" ")[0] for line in gcc_help]
    supported_versions = gcc_help
    return supported_versions


def get_most_recent_cpp_version() -> str:
    """Returns the most recent C++ standard supported by the system."""
    all_versions = get_gcc_supported_standard()
    # keep those with c++<number> only and return the one with the highest
    # number
    all_versions = [ver for ver in all_versions if re.match(r"^c\+\+\d+$", ver)]
    cpp_versions = [ver.replace("c++", "") for ver in all_versions]
    # add the prefix to each number, either 19 or 20 depending on the number
    # if the number is greater or equal than 89 (1989) then it is 19, else 20
    cpp_versions = [
        f"19{ver}" if int(ver) >= 89 else f"20{ver}" for ver in cpp_versions
    ]
    cpp_versions = sorted(cpp_versions)
    if len(cpp_versions) == 0:
        return "no gcc found in"
    most_recent_cpp_version = cpp_versions[-1][-2:]
    return f"c++{most_recent_cpp_version}"


MOST_RECENT_GCC_STD_VERSION = get_most_recent_cpp_version()


class CPPTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a C++ Fuzzer"
        if kwargs["template"] == "fuzzing_with_config_file":
            config_dict = kwargs["config_dict"]
            self.prompt_used = self._create_prompt_from_config(config_dict)
            self.config_dict = config_dict
        elif kwargs["template"] == "cpp_span":
            self.prompt_used = cpp_span
        elif kwargs["template"] == "cpp_is_scoped_enum":
            self.prompt_used = cpp_is_scoped_enum
        elif kwargs["template"] == "cpp_optional":
            self.prompt_used = cpp_optional
        elif kwargs["template"] == "cpp_variant":
            self.prompt_used = cpp_variant
        elif kwargs["template"] == "cpp_expected":
            self.prompt_used = cpp_expected
        elif kwargs["template"] == "cpp_expected_example":
            self.prompt_used = cpp_expected_example
        elif kwargs["template"] == "cpp_apply":
            self.prompt_used = cpp_apply
        elif kwargs["template"] == "cpp_23":
            self.prompt_used = cpp_23
        else:
            raise NotImplementedError

    def write_back_file(self, code):
        try:
            with open(
                "/tmp/temp{}.cpp".format(self.CURRENT_TIME), "w", encoding="utf-8"
            ) as f:
                f.write(code)
        except:
            pass
        return "/tmp/temp{}.cpp".format(self.CURRENT_TIME)

    def wrap_prompt(self, prompt: str) -> str:
        return f"/* {prompt} */\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"/* {prompt} */"

    def filter(self, code) -> bool:
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        if self.prompt_used["target_api"] not in clean_code:
            return False
        return True

    def clean(self, code: str) -> str:
        code = comment_remover(code)
        return code

    # remove any comments, or blank lines
    def clean_code(self, code: str) -> str:
        code = comment_remover(code)
        code = "\n".join(
            [
                line
                for line in code.split("\n")
                if line.strip() != "" and line.strip() != self.prompt_used["begin"]
            ]
        )
        return code

    def validate_compiler_with_opt(self, compiler, filename) -> (FResult, str):

        base_result, base_message = self.validate_compiler(compiler, filename)
        if base_result == FResult.TIMED_OUT:
            return base_result, base_message

        results = [base_result]
        messages = [f"base\n{base_message}"]

        for opt in ["-O3", "-O2", "-O1"]:
            try:
                exit_code = subprocess.run(
                    f"{compiler} -std={MOST_RECENT_GCC_STD_VERSION} -x c++ {opt} {filename} -o /tmp/out{self.CURRENT_TIME}",
                    shell=True,
                    capture_output=True,
                    encoding="utf-8",
                    timeout=5,
                    text=True,
                )
            except subprocess.TimeoutExpired:
                results.append(FResult.TIMED_OUT)
                messages.append(f"Optimization {opt} Timeout")
                continue
            if exit_code.returncode == 0:
                results.append(FResult.SAFE)
                messages.append(f"Optimization {opt} is safe")
            elif exit_code.returncode != 0:
                results.append(FResult.FAILURE)
                messages.append(f"Optimization {opt}:\n{exit_code.stderr}")

        if (
            FResult.ERROR in results or FResult.FAILURE in results
        ) and FResult.SAFE in results:
            return FResult.ERROR, "leading to incorrect optimization!" + "\n".join(
                messages
            )

        return base_result, "\n".join(messages)

    def validate_compiler(self, compiler, filename) -> (FResult, str):
        # check without -c option (+ linking)
        try:
            exit_code = subprocess.run(
                f"{compiler} -x c++ -std={MOST_RECENT_GCC_STD_VERSION} {filename} -o /tmp/out{self.CURRENT_TIME}",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=5,
                text=True,
            )
        except subprocess.TimeoutExpired as te:
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
            return FResult.TIMED_OUT, compiler

        if exit_code.returncode == 1:
            if "undefined reference to `main'" in exit_code.stderr:
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        code = f.read()
                except:
                    pass
                self.write_back_file(code + main_code)
                exit_code = subprocess.run(
                    f"{compiler} -std={MOST_RECENT_GCC_STD_VERSION} -x c++ /tmp/temp{self.CURRENT_TIME}.cpp -o /tmp/out{self.CURRENT_TIME}",
                    shell=True,
                    capture_output=True,
                    encoding="utf-8",
                    text=True,
                )
                if exit_code.returncode == 0:
                    return FResult.SAFE, "its safe"
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

        return FResult.SAFE, "its safe"

    def validate_individual(self, filename) -> (FResult, str):
        gcc_fresult, gcc_msg = self.validate_compiler("g++", filename)
        clang_fresult, clang_msg = self.validate_compiler("clang++", filename)
        if gcc_fresult == FResult.SAFE and clang_fresult == FResult.SAFE:
            return FResult.SAFE, "its safe"
        elif gcc_fresult == FResult.ERROR or clang_fresult == FResult.ERROR:
            return FResult.ERROR, f"gcc: {gcc_msg}\nclang:{clang_msg}"
        elif gcc_fresult != FResult.TIMED_OUT and clang_fresult == FResult.TIMED_OUT:
            return FResult.ERROR, f"clang timed out but gcc was fine"
        elif gcc_fresult == FResult.TIMED_OUT and clang_fresult != FResult.TIMED_OUT:
            return FResult.ERROR, f"gcc timed out but clang was fine"
        elif gcc_fresult == FResult.FAILURE or clang_fresult == FResult.FAILURE:
            return FResult.FAILURE, f"gcc: {gcc_msg}\nclang:{clang_msg}"
        else:
            return FResult.TIMED_OUT, f"both timed out"

    def check_syntax_valid(self, code):
        with open("/tmp/temp{}.cpp".format(self.CURRENT_TIME), "w") as f:
            f.write(code)
        try:
            exit_code = subprocess.run(
                "g++ -std={} -c -fsyntax-only {}".format(
                    MOST_RECENT_GCC_STD_VERSION,
                    "/tmp/temp{}.cpp".format(self.CURRENT_TIME),
                ),
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if exit_code.returncode == 0:
                return True
            else:
                print(exit_code.stderr)
                return False
        except subprocess.TimeoutExpired as te:
            pname = "'temp{}.cpp'".format(self.CURRENT_TIME)
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
            return False
