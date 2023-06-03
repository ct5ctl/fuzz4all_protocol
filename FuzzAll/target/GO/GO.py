import subprocess
import time
from typing import List, Union

import torch

from FuzzAll.target.GO.template import go_atomic
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL
from FuzzAll.util.util import comment_remover


class GOTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs["template"] == "go_atomic":
            self.prompt_used = go_atomic
        else:
            raise NotImplementedError
        # TODO: strategies

    def validate_prompt(self, prompt: str):
        # TODO
        return 0

    def wrap_prompt(self, prompt: str) -> str:
        return (
            f"// {prompt}\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"
        )

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

    def filter(self, code: str) -> bool:
        code = code.replace(self.prompt_used["begin"], "").strip()
        code = comment_remover(code)
        if self.prompt_used["target_api"] not in code:
            return False
        return True

    def clean_code(self, code: str) -> str:
        code = code.replace(self.prompt_used["begin"], "").strip()
        code = comment_remover(code)
        code = "\n".join([line for line in code.split("\n") if line.strip() != ""])
        return code

    def update(self, **kwargs):
        new_code = ""
        for result, code in kwargs["prev"]:
            if result == FResult.SAFE and self.filter(code):
                new_code = self.clean_code(code)
        if new_code != "":
            self.prompt = (
                self.initial_prompt
                + "\n"
                + new_code
                + "\n"
                + self.prompt_used["separator"]
                + "\n"
                + self.prompt_used["begin"]
            )

    def write_back_file(self, code):
        try:
            with open(
                "/tmp/temp{}.go".format(self.CURRENT_TIME), "w", encoding="utf-8"
            ) as f:
                f.write(code)
        except:
            pass

    def validate_individual(self, filename) -> (FResult, str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except:
            pass
        self.write_back_file(code)
        try:
            exit_code = subprocess.run(
                f"go run /tmp/temp{self.CURRENT_TIME}.go",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=5,
                text=True,
            )
        except subprocess.TimeoutExpired as te:
            pname = f"'temp{self.CURRENT_TIME}'"
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
            return FResult.TIMED_OUT, "go"
        if exit_code.returncode == 1:
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode == 0:
            return FResult.SAFE, exit_code.stdout
        else:
            return FResult.ERROR, exit_code.stderr
