import subprocess

from target.base_target import Target
from target.base_target import FResult


class GCCTarget(Target):

    def validate_individual(self, filename):
        self.logger.logo("Validating {} ...".format(filename))

        exit_code = subprocess.run("gcc -c {} -o testbed/out".format(filename), shell=True,
                                   capture_output=True,
                                   encoding="utf-8",
                                   text=True)
        if exit_code.returncode == 1:
            return FResult.FAILURE, "failed to compile"
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

        for op in ['O1', 'O2', 'O3']:
            exit_code = subprocess.run("gcc -{} -c {} -o testbed/out{}".format(op, filename, op), shell=True,
                                       capture_output=True,
                                       encoding="utf-8",
                                       text=True)
            if exit_code.returncode != 0:
                return FResult.ERROR, exit_code.stderr

        # check without -c option (+ linking)
        exit_code = subprocess.run("gcc {} -o testbed/out".format(filename), shell=True,
                                   capture_output=True,
                                   encoding="utf-8",
                                   text=True)
        if exit_code.returncode == 1:
            return FResult.FAILURE, "failed to compile"
        elif exit_code.returncode != 0:
            return FResult.ERROR, exit_code.stderr

        for op in ['O1', 'O2', 'O3']:
            exit_code = subprocess.run("gcc {} -{} -o testbed/out{}".format(filename, op, op), shell=True,
                                       capture_output=True,
                                       encoding="utf-8",
                                       text=True)
            if exit_code.returncode != 0:
                return FResult.ERROR, "{} failed to compile".format(op)


        # try:
        #     # TODO: maybe solve alot of user input related code, its causing many timeouts
        #     base_code = subprocess.run("./testbed/out",
        #                                shell=True,
        #                                capture_output=True,
        #                                text=True,
        #                                encoding="utf-8",
        #                                timeout=self.timeout if self.timeout else None)
        # except subprocess.TimeoutExpired as te:
        #     subprocess.run(["ps -ef | grep 'testbed/out' | grep -v grep | awk '{print $2}'"], shell=True)
        #     subprocess.run(["ps -ef | grep 'testbed/out' | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
        #                    shell=True)  # kill all tests thank you
        #     return FResult.FAILURE, "timed out"
        # except UnicodeDecodeError as ue:
        #     return FResult.FAILURE, "unicode decode error"
        #
        # if base_code.returncode != 0:
        #     return FResult.ERROR, base_code.stderr
        #
        # # optimization running
        # for op in ['O1', 'O2', 'O3']:
        #     exit_code = subprocess.run("gcc {} -{} -o testbed/out{}".format(filename, op, op), shell=True,
        #                                capture_output=True,
        #                                encoding="utf-8",
        #                                text=True)
        #     if exit_code.returncode != 0:
        #         return FResult.ERROR, "{} failed to compile".format(op)
        #     try:
        #         op_code = subprocess.run("./testbed/out{}".format(op),
        #                                    shell=True,
        #                                    capture_output=True,
        #                                    text=True,
        #                                    encoding="utf-8",
        #                                    timeout=self.timeout if self.timeout else None)
        #     except subprocess.TimeoutExpired as te:
        #         pname = "'testbed/out{}'".format(op)
        #         subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"], shell=True)
        #         subprocess.run(["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
        #                        shell=True)  # kill all tests thank you
        #         return FResult.ERROR, "{} timed out".format(op)
        #     except UnicodeDecodeError as ue:
        #         return FResult.ERROR, "{} unicode decoder error".format(op)
        #
        #     if op_code.stdout != base_code.stdout:
        #         return FResult.ERROR, "{} different results:\nNo Optimization: {}\nOptimization: {}"\
        #             .format(op, base_code.stdout, op_code.stdout)

        return FResult.SAFE, "its safe"

