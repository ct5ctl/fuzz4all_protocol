import subprocess
import time
from typing import List, Union

import torch

# TODO: fix template to within their own folder, kinda of like a dump folder for user
from FuzzAll.target.CPP.template import (
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


class GPP12Target(Target):
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
        else:
            raise NotImplementedError
        # TODO: strategies

    def write_back_file(self, code):
        try:
            with open(
                "/tmp/temp{}.cpp".format(self.CURRENT_TIME), "w", encoding="utf-8"
            ) as f:
                f.write(code + main_code)
        except:
            pass

    def validate_prompt(self, prompt):
        # TODO
        return 0

    def wrap_prompt(self, prompt: str) -> str:
        return f"/* {prompt} */\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        return f"/* {prompt} */"

    def generate(self, **kwargs) -> Union[List[str], bool]:
        try:
            fos = self.generate_model()
        except RuntimeError:
            # catch cuda out of memory error.
            self.m_logger.logo("cuda out of memory...", level=LEVEL.INFO)
            del self.model
            torch.cuda.empty_cache()
            return False
        new_fos = []
        for fo in fos:
            self.g_logger.logo("========== sample =========", level=LEVEL.VERBOSE)
            new_fos.append(self.prompt_used["begin"] + "\n" + fo)
            self.g_logger.logo(
                self.prompt_used["begin"] + "\n" + fo, level=LEVEL.VERBOSE
            )
            self.g_logger.logo("========== sample =========", level=LEVEL.VERBOSE)
        return new_fos

    def filter(self, code) -> bool:
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        if self.prompt_used["target_api"] not in clean_code:
            return False
        return True

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

    def validate_individual(self, filename) -> (FResult, str):
        # check without -c option (+ linking)
        try:
            exit_code = subprocess.run(
                "g++ -x c++ -std=c++23 {} -o /tmp/out{}".format(
                    filename, self.CURRENT_TIME
                ),
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=5,
                text=True,
            )
        except subprocess.TimeoutExpired as te:
            pname = "'{}'".format(filename)
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
            return FResult.TIMED_OUT, "gcc"

        if exit_code.returncode == 1:
            if "undefined reference to `main'" in exit_code.stderr:
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        code = f.read()
                except:
                    pass
                self.write_back_file(code)
                exit_code = subprocess.run(
                    "g++ -std=c++23 -x c++ /tmp/temp{}.cpp -o /tmp/out{}".format(
                        self.CURRENT_TIME, self.CURRENT_TIME
                    ),
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
