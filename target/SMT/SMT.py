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
        return True