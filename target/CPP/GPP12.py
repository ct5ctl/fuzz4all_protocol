import subprocess

from target.base_target import Target
from target.base_target import FResult

main_code = """
int main(){
return 0;
}
"""


class GPP12Target(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a C++ Fuzzer"

    def write_back_file(self, code):
        with open("temp{}.cpp".format(self.CURRENT_TIME), "w") as f:
            f.write(code+main_code)

    def validate_individual(self, filename) -> (FResult, str):
        self.logger.logo("Validating {} ...".format(filename))
        # check without -c option (+ linking)
        exit_code = subprocess.run("g++ {} -std=c++23 -o testbed/out".format(filename), shell=True,
                                   capture_output=True,
                                   encoding="utf-8",
                                   text=True)
        if exit_code.returncode == 1:
            if "undefined reference to `main'" in exit_code.stderr:
                with open(filename, "r") as f:
                    code = f.read()
                self.write_back_file(code)
                exit_code = subprocess.run("g++ temp{}.cpp -std=c++23 -o testbed/out".format(self.CURRENT_TIME), shell=True,
                                           capture_output=True,
                                           encoding="utf-8",
                                           text=True)
                if exit_code.returncode == 0:
                    return FResult.SAFE, "its safe"
            return FResult.FAILURE, exit_code.stderr
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

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