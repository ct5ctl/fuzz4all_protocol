import subprocess

from target.base_target import Target
from target.base_target import FResult


class GPP12Target(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a C++ Fuzzer"

    def validate_individual(self, filename) -> (FResult, str):
        self.logger.logo("Validating {} ...".format(filename))
        exit_code = subprocess.run("g++ -c {} -std=c++23 -o testbed/out".format(filename), shell=True,
                                   capture_output=True,
                                   encoding="utf-8",
                                   text=True)
        if exit_code.returncode == 1:
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

        for op in ['O1', 'O2', 'O3']:
            exit_code = subprocess.run("g++ -{} -c {} -std=c++23 -o testbed/out{}".format(op, filename, op), shell=True,
                                       capture_output=True,
                                       encoding="utf-8",
                                       text=True)
            if exit_code.returncode != 0:
                return FResult.ERROR, exit_code.stderr

        # check without -c option (+ linking)
        exit_code = subprocess.run("g++ {} -std=c++23 -o testbed/out".format(filename), shell=True,
                                   capture_output=True,
                                   encoding="utf-8",
                                   text=True)
        if exit_code.returncode == 1:
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

        for op in ['O1', 'O2', 'O3']:
            exit_code = subprocess.run("g++ {} -std=c++23 -{} -o testbed/out{}".format(filename, op, op), shell=True,
                                       capture_output=True,
                                       encoding="utf-8",
                                       text=True)
            if exit_code.returncode != 0:
                return FResult.ERROR, "{} failed to compile".format(op)

        return FResult.SAFE, "its safe"

    def check_syntax_valid(self, code):
        with open("temp{}.cpp".format(self.CURRENT_TIME), "w") as f:
            f.write(code)
        try:
            exit_code = subprocess.run("g++ -std=c++23 -c -fsyntax-only {}".format("temp{}.cpp".format(self.CURRENT_TIME)),
                                       shell=True, capture_output=True, text=True,
                                       timeout=5)
            if exit_code.returncode == 0:
                return True
            else:
                print(exit_code.stderr)
                return False
        except subprocess.TimeoutExpired as te:
            pname = "'temp{}.cpp'".format(self.CURRENT_TIME)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"], shell=True)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
                           shell=True)  # kill all tests thank you
            return False