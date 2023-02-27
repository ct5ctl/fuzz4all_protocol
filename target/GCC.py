import subprocess

from target.base_target import Target
from target.base_target import FResult


class GCCTarget(Target):

    def validate_individual(self, filename):
        self.logger.logo("Validating {} ...".format(filename))
        exit_code = subprocess.run("gcc {} -o testbed/out".format(filename), shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        if exit_code.returncode != 0:
            return FResult.FAILURE, "failed to compile"

        try:
            exit_code = subprocess.run("./testbed/out",
                                       shell=True,
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL,
                                       timeout=self.timeout if self.timeout else None)
        except subprocess.TimeoutExpired as te:
            subprocess.run(["ps -ef | grep 'testbed/out' | grep -v grep | awk '{print $2}'"], shell=True)
            subprocess.run(["ps -ef | grep 'testbed/out' | grep -v grep | awk '{print $2}' | xargs -r kill -9"],
                   shell=True)  # kill all tests thank you
            return FResult.FAILURE, "timed out"
        if exit_code.returncode != 0:
            return FResult.ERROR, exit_code

        return FResult.SAFE, "its safe"
