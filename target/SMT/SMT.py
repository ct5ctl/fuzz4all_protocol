import subprocess

from target.base_target import Target
from target.base_target import FResult


class SMTTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a SMT Fuzzer"

    def validate_individual(self, filename) -> (FResult, str):
        # TODO: differential testing with libraries
        pass

    def check_syntax_valid(self, code):
        # TODO
        with open("temp{}.smt2".format(self.CURRENT_TIME), "w") as f:
            f.write(code)
        try:
            exit_code = subprocess.run(
                "cvc5-Linux --lang smt2 {}".format("temp{}.smt2".format(self.CURRENT_TIME)),
                shell=True, capture_output=True, text=True,
                timeout=5)
            if exit_code.returncode == 0:
                return True
            else:
                print(exit_code.stdout)
                return False
        except subprocess.TimeoutExpired as te:
            pname = "'temp{}.smt2'".format(self.CURRENT_TIME)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"], shell=True)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
                           shell=True)  # kill all tests thank you
            return False
