import subprocess
import time
from re import search
from typing import List, Union

import torch

from FuzzAll.target.target import FResult, Target
from FuzzAll.util.Logger import LEVEL
from FuzzAll.util.util import comment_remover


class JAVATarget(Target):
    def __init__(self, **kwags):
        super().__init__(**kwags)
        # TODO
        raise NotImplementedError

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

    def clean_code(self, code: str) -> str:
        code = comment_remover(code)
        code = "\n".join([line for line in code.split("\n") if line.strip() != ""])
        return code

    def write_back_file(self, code, write_back_name):
        try:
            with open(write_back_name, "w", encoding="utf-8") as f:
                f.write(code)
        except:
            pass

    # If there exists a public class, ensure file name matches
    def determine_file_name(self, code):
        public_class_name = search("\s*public(\s)+class(\s)+([^\s\{]+)", code)
        if public_class_name == None:
            # No public class found, return standard write back file name
            return "/tmp/temp{}.java".format(self.CURRENT_TIME)
        # Public class is found, ensure that file name matches public class name
        return "/tmp/temp{0}/{1}.java".format(
            self.CURRENT_TIME, public_class_name[0].split()[-1]
        )

    def validate_individual(self, filename) -> (FResult, str):
        write_back_name = ""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
                write_back_name = self.determine_file_name(code)
                self.write_back_file(code, write_back_name)
        except:
            pass

        try:
            exit_code = subprocess.run(
                f"javac {write_back_name}",
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
            return FResult.TIMED_OUT, "java"
        if exit_code.returncode == 1:
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode == 0:
            return FResult.SAFE, exit_code.stdout
        else:
            return FResult.ERROR, exit_code.stderr
