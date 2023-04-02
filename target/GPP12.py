import subprocess

from target.base_target import Target
from target.base_target import FResult


class GPP12Target(Target):

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