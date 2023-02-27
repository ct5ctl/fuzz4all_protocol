import os
import glob

from enum import Enum
from engine.util.Logger import Logger


class FResult(Enum):
    SAFE = 1  # validation returns okay
    FAILURE = 2  # validation contains error (something wrong with validation)
    ERROR = 3  # validation returns a potential error (look into)


# base class file for target, used for user defined system targets
# the point is to separately define oracles
class Target(object):
    def __init__(self, language="c", timeout=10, folder="/"):
        self.language = language
        self.folder = folder
        self.timeout = timeout
        self.logger = Logger(self.folder)

    def validate_individual(self, filename) -> (FResult, str):
        raise NotImplementedError

    def validate_all(self):
        for fuzz_output in glob.glob(self.folder + "/*.{}".format(self.language)):
            f_result, message = self.validate_individual(fuzz_output)
            if f_result == FResult.SAFE:
                self.logger.logo("{} is safe".format(fuzz_output))
            elif f_result == FResult.FAILURE:
                self.logger.logo("{} failed validation with error message: {}".format(fuzz_output, message))
            elif f_result == FResult.ERROR:
                self.logger.logo("{} has potential error!\nerror message:\n{}".format(fuzz_output, message))
