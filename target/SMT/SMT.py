import subprocess

from target.base_target import Target
from target.base_target import FResult


def _check_sat(stdout):
    sat = ""
    for x in stdout.splitlines():
        if x.strip() == "unsat" or x.strip() == "sat":
            sat = x.strip()
            break
    return sat


# why is this needed? because sometimes the error could be suppressed in
# the return code of the smt solver however such error still exists.
def _check_error(stdout):
    error = False
    for x in stdout.splitlines():
        if x.strip().startswith("(error"):
            error = True
            break
    return error


# ignore cvc5 unary minus
# TODO: add additional rewriting rule to fix this
def _check_cvc5_parse_error(stdout):
    error = False
    for x in stdout.splitlines():
        if "Parse Error:" in x.strip():
            error = True
            break
    return error


# remove logic set which can lead to parse errors
def clean_logic(code):
    clean_code = "\n".join([x for x in code.splitlines() if not x.startswith("(set-logic")])
    return clean_code


class SMTTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SYSTEM_MESSAGE = "You are a SMT Fuzzer"

    def write_back_file(self, code):
        with open("temp{}.smt2".format(self.CURRENT_TIME), "w") as f:
            f.write(code)

    def validate_individual(self, filename) -> (FResult, str):
        self.logger.logo("Validating {} ...".format(filename))
        with open(filename, "r") as f:
            code = f.read()
        self.write_back_file(clean_logic(code))
        try:
            cvc_exit_code = subprocess.run(
                    "cvc5-Linux -m -i -q --check-models --lang smt2 temp{}.smt2".format(self.CURRENT_TIME),
                    shell=True, capture_output=True, text=True,
                    timeout=5)
        except subprocess.TimeoutExpired as te:
            pname = "'temp{}.smt2'".format(self.CURRENT_TIME)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"], shell=True)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
                           shell=True)  # kill all tests thank you
            return FResult.TIMED_OUT, "CVC5 Timed out"

        try:
            z3_exit_code = subprocess.run(
                "z3 model_validate=true temp{}.smt2".format(self.CURRENT_TIME),
                shell=True, capture_output=True, text=True,
                timeout=5)
        except subprocess.TimeoutExpired as te:
            pname = "'temp{}.smt2'".format(self.CURRENT_TIME)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"], shell=True)
            subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
                           shell=True)  # kill all tests thank you
            return FResult.TIMED_OUT, "Z3 Timed out"

        # failed compilation
        if z3_exit_code.returncode == 1 and cvc_exit_code.returncode == 1:
            return FResult.FAILURE, "Z3:\n{}\nCVC5:\n{}".format(z3_exit_code.stdout, cvc_exit_code.stdout)

        # first grab the sat results, because some error can be tolerable for sat solving actually
        z3_sat = _check_sat(z3_exit_code.stdout)
        cvc5_sat = _check_sat(cvc_exit_code.stdout)
        if (z3_sat != "" and cvc5_sat != "") and z3_sat != cvc5_sat:
            return FResult.ERROR, "Different SAT Results. Z3: {} CVC5: {}".format(z3_sat, cvc5_sat)
        elif (z3_sat != "" and cvc5_sat != "") and z3_sat == cvc5_sat:
            return FResult.SAFE, "its safe"

        if z3_exit_code.returncode == 1:
            if _check_error(cvc_exit_code.stdout):
                return FResult.FAILURE, "Z3:\n{}\nCVC5:\n{}".format(z3_exit_code.stdout, cvc_exit_code.stdout)
            else:
                return FResult.ERROR, "CVC5 is fine:\n{}\n but Z3 outputs:\n{}".format(cvc_exit_code.stdout,
                                                                                       z3_exit_code.stdout)
        elif cvc_exit_code.returncode == 1:
            if _check_error(z3_exit_code.stdout):
                return FResult.FAILURE, "Z3:\n{}\nCVC5:\n{}".format(z3_exit_code.stdout, cvc_exit_code.stdout)
            else:
                if _check_cvc5_parse_error(cvc_exit_code.stdout):
                    return FResult.FAILURE, "Z3:\n{}\nCVC5:\n{}".format(z3_exit_code.stdout, cvc_exit_code.stdout)
                return FResult.ERROR, "Z3 is fine:\n{}\n but CVC5 outputs:\n{}".format(z3_exit_code.stdout,
                                                                                       cvc_exit_code.stdout)

        return FResult.SAFE, "its safe"

    def check_syntax_valid(self, code):
        with open("temp{}.smt2".format(self.CURRENT_TIME), "w") as f:
            f.write(clean_logic(code))
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
