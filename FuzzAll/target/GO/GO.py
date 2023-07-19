import subprocess
import time
from typing import List, Union

import torch

from FuzzAll.target.GO.template import (
    go_atomic,
    go_big_math,
    go_bytes,
    go_heap,
    go_maphash,
    go_reflect,
    go_std,
    go_strconv,
)
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL
from FuzzAll.util.util import comment_remover


class GOTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs["template"] == "fuzzing_with_config_file":
            config_dict = kwargs["config_dict"]
            self.prompt_used = self._create_prompt_from_config(config_dict)
            self.config_dict = config_dict
        elif kwargs["template"] == "go_atomic":
            self.prompt_used = go_atomic
        elif kwargs["template"] == "go_heap":
            self.prompt_used = go_heap
        elif kwargs["template"] == "go_big_math":
            self.prompt_used = go_big_math
        elif kwargs["template"] == "go_reflect":
            self.prompt_used = go_reflect
        elif kwargs["template"] == "go_maphash":
            self.prompt_used = go_maphash
        elif kwargs["template"] == "go_strconv":
            self.prompt_used = go_strconv
        elif kwargs["template"] == "go_bytes":
            self.prompt_used = go_bytes
        elif kwargs["template"] == "go_std":
            self.prompt_used = go_std
        else:
            raise NotImplementedError

        self.special_eos = "package main"

    def wrap_prompt(self, prompt: str) -> str:
        return (
            f"// {prompt}\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"
        )

    def wrap_in_comment(self, prompt: str) -> str:
        return f"// {prompt}"

    def filter(self, code: str) -> bool:
        code = code.replace(self.prompt_used["begin"], "").strip()
        code = comment_remover(code)
        if self.prompt_used["target_api"] not in code:
            return False
        return True

    def clean(self, code: str) -> str:
        code = comment_remover(code)
        return code

    def clean_code(self, code: str) -> str:
        code = code.replace(self.prompt_used["begin"], "").strip()
        code = comment_remover(code)
        code = "\n".join([line for line in code.split("\n") if line.strip() != ""])
        return code

    def write_back_file(self, code):
        try:
            with open(
                "/tmp/temp{}.go".format(self.CURRENT_TIME), "w", encoding="utf-8"
            ) as f:
                f.write(code)
        except:
            pass
        return "/tmp/temp{}.go".format(self.CURRENT_TIME)

    def validate_individual(self, filename) -> (FResult, str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except:
            pass
        self.write_back_file(code)
        try:
            exit_code = subprocess.run(
                f"go build -o /tmp/temp{self.CURRENT_TIME} /tmp/temp{self.CURRENT_TIME}.go",
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
        except UnicodeDecodeError as ue:
            return FResult.FAILURE, "decoding error"
        if exit_code.returncode == 1:
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode == 0:
            return FResult.SAFE, exit_code.stdout
        else:
            return FResult.ERROR, exit_code.stderr
