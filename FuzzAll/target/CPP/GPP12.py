import subprocess
import time
from typing import List

from FuzzAll.model import make_model
from FuzzAll.target.CPP.template import cpp_span
from FuzzAll.target.target import FResult, Target
from FuzzAll.util.api_request import create_chatgpt_config, request_engine
from FuzzAll.util.util import comment_remover, simple_parse

main_code = """
int main(){
return 0;
}
"""


def _create_chatgpt_docstring_template(
    system_message: str, user_message: str, docstring: str, example: str, first: str
):
    messages = [{"role": "system", "content": system_message}]
    messages.append({"role": "user", "content": docstring})
    messages.append({"role": "user", "content": example})
    if first != "":
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": "```\n{}\n```".format(first)})
    messages.append({"role": "user", "content": user_message})
    return messages


class GPP12Target(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None  # to be declared
        self.SYSTEM_MESSAGE = "You are a C++ Fuzzer"
        # stateful objects that change
        self.prompt = ""
        if kwargs["template"] == "cpp_span":
            self.prompt_used = cpp_span
        else:
            raise NotImplementedError
        self.prompt = (
            self.prompt_used["docstring"] + "\n" + self.prompt_used["separator"]
        )
        self.batch_size = kwargs["bs"]
        self.temperature = kwargs["temperature"]
        # TODO: strategies

    def write_back_file(self, code):
        with open("/tmp/temp{}.cpp".format(self.CURRENT_TIME), "w") as f:
            f.write(code + main_code)

    def initialize(self):
        self.g_logger.logo("Initializing ... this may take a while ...")
        self.model = make_model()
        self.g_logger.logo("done")

    def generate_chatgpt(self) -> List[str]:
        messages = _create_chatgpt_docstring_template(
            self.SYSTEM_MESSAGE,
            self.prompt_used["separator"],
            self.prompt_used["docstring"],
            self.prompt_used["example_code"],
            "",
        )
        config = create_chatgpt_config(
            prev={}, messages=messages, max_tokens=512, temperature=1.3
        )
        ret = request_engine(config)
        func = comment_remover(simple_parse(ret["choices"][0]["message"]["content"]))
        return [func]

    def generate_model(self) -> List[str]:
        return self.model.generate(
            self.prompt,
            batch_size=self.batch_size,
            temperature=self.temperature,
            max_length=1024,
        )

    def generate(self, **kwargs) -> List[str]:
        fos = self.generate_model()
        for fo in fos:
            self.g_logger.logo("========== sample =========")
            self.g_logger.logo(fo)
            self.g_logger.logo("========== sample =========")
        return fos

    def validate_individual(self, filename) -> (FResult, str):
        self.v_logger.logo("Validating {} ...".format(filename))
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
                with open(filename, "r") as f:
                    code = f.read()
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
