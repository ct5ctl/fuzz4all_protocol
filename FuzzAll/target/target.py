import glob
import time
from enum import Enum
from typing import List

from rich.progress import track

from FuzzAll.util.Logger import Logger


class FResult(Enum):
    SAFE = 1  # validation returns okay
    FAILURE = 2  # validation contains error (something wrong with validation)
    ERROR = 3  # validation returns a potential error (look into)
    TIMED_OUT = 10  # timed out, can be okay in certain targets


# base class file for target, used for user defined system targets
# the point is to separately define oracles/fuzzing specific functions/and usages
# target should be a stateful objects which has some notion of history (keeping a state of latest prompts)
class Target(object):
    def __init__(self, language="c", timeout=10, folder="/", **kwargs):
        self.language = language
        self.folder = folder
        self.timeout = timeout
        # loggers
        self.g_logger = Logger(self.folder, validation=False, verbose=kwargs["verbose"])
        self.v_logger = Logger(self.folder, validation=True, verbose=kwargs["verbose"])
        self.CURRENT_TIME = time.time()
        # to be overwritten
        self.SYSTEM_MESSAGE = "You are a Fuzzer."

    # used for fuzzing to check valid syntax
    def check_syntax_valid(self, code) -> bool:
        # by default return true as there might not be need for syntax check
        # however such check might be beneficial.
        return True

    # initialize through either some templates or auto-prompting to determine prompts
    def initialize(self):
        raise NotImplementedError

    # generation
    def generate(self, **kwargs) -> List[str]:
        raise NotImplementedError

    # update
    def update(self, **kwargs):
        raise NotImplementedError

    # validation
    def validate_individual(self, filename) -> (FResult, str):
        raise NotImplementedError

    def parse_validation_message(self, f_result, message, file_name):
        if f_result == FResult.SAFE:
            self.v_logger.logo("{} is safe".format(file_name))
        elif f_result == FResult.FAILURE:
            self.v_logger.logo(
                "{} failed validation with error message: {}".format(file_name, message)
            )
        elif f_result == FResult.ERROR:
            self.v_logger.logo(
                "{} has potential error!\nerror message:\n{}".format(file_name, message)
            )
        elif f_result == FResult.TIMED_OUT:
            self.v_logger.logo("{} timed out".format(file_name))

    def validate_all(self):
        for fuzz_output in track(
            glob.glob(self.folder + "/*.fuzz"),
            description="Validating",
        ):
            f_result, message = self.validate_individual(fuzz_output)
            self.parse_validation_message(f_result, message, fuzz_output)
