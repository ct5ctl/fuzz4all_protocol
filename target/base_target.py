import glob
import time

from enum import Enum
from engine.util.Logger import Logger


class FResult(Enum):
    SAFE = 1  # validation returns okay
    FAILURE = 2  # validation contains error (something wrong with validation)
    ERROR = 3  # validation returns a potential error (look into)
    TIMED_OUT = 10  # timed out, can be okay in certain targets


# base class file for target, used for user defined system targets
# the point is to separately define oracles/fuzzing specific functions/and usages
class Target(object):
    def __init__(self, language="c", timeout=10, folder="/", validation=False):
        self.language = language
        self.folder = folder
        self.timeout = timeout
        self.logger = Logger(self.folder, validation=validation)
        self.CURRENT_TIME = time.time()
        # to be overwritten
        self.SYSTEM_MESSAGE = "You are a Fuzzer."

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
            elif f_result == FResult.TIMED_OUT:
                self.logger.logo("{} timed out".format(fuzz_output))

    # used for fuzzing to check valid syntax
    def check_syntax_valid(self, code):
        # by default return true as there might not be need for syntax check
        # however such check might be beneficial.
        return True
