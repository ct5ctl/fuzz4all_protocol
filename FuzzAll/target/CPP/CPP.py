import subprocess
import time
from typing import List, Union

import torch

# TODO: fix template to within their own folder, kinda of like a dump folder for user
from FuzzAll.target.CPP.template import (
    cpp_23,
    cpp_apply,
    cpp_expected,
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


class CPPTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a C++ Fuzzer"
        if kwargs["template"] == "cpp_span":
            self.prompt_used = cpp_span
        elif kwargs["template"] == "cpp_is_scoped_enum":
            self.prompt_used = cpp_is_scoped_enum
        elif kwargs["template"] == "cpp_optional":
            self.prompt_used = cpp_optional
        elif kwargs["template"] == "cpp_variant":
            self.prompt_used = cpp_variant
        elif kwargs["template"] == "cpp_expected":
            self.prompt_used = cpp_expected
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

    def validate_compiler(self, compiler, filename) -> (FResult, str):
        # check without -c option (+ linking)
        try:
            exit_code = subprocess.run(
                f"{compiler} -x c++ -std=c++23 {filename} -o /tmp/out{self.CURRENT_TIME}",
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
                    f"{compiler} -std=c++23 -x c++ /tmp/temp{self.CURRENT_TIME}.cpp -o /tmp/out{self.CURRENT_TIME}",
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
                "g++ -std=c++23 -c -fsyntax-only {}".format(
                    "/tmp/temp{}.cpp".format(self.CURRENT_TIME)
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
