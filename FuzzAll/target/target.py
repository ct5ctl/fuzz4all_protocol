import glob
import os
import time
from enum import Enum
from typing import List, Union

from rich.progress import track

from FuzzAll.model import make_model
from FuzzAll.util.api_request import create_config, request_engine
from FuzzAll.util.Logger import LEVEL, Logger
from FuzzAll.util.util import (
    comment_remover,
    create_chatgpt_docstring_template,
    simple_parse,
)


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
        self.g_logger = Logger(self.folder, "log_generation.txt", level=kwargs["level"])
        self.v_logger = Logger(self.folder, "log_validation.txt", level=kwargs["level"])
        # main logger for system messages
        self.m_logger = Logger(self.folder, "log.txt")
        self.CURRENT_TIME = time.time()
        self.SYSTEM_MESSAGE = None
        self.AP_SYSTEM_MESSAGE = "You are an auto-prompting tool"
        self.AP_INSTRUCTION = (
            "Please summarize the above documentation in a concise manner to describe the usage and "
            "functionality of the target "
        )
        self.prompt_used = None
        self.batch_size = kwargs["bs"]
        self.temperature = kwargs["temperature"]
        self.model = None
        self.prompt = None
        self.initial_prompt = None

    # used for fuzzing to check valid syntax
    def check_syntax_valid(self, code: str) -> bool:
        # by default return true as there might not be need for syntax check
        # however such check might be beneficial.
        return True

    # each target defines their way of validating prompts
    def validate_prompt(self, prompt: str):
        raise NotImplementedError

    # each target defines their way of validating prompts
    # for example we might want to encode the prompt as a docstring comment to facilitate better generation using
    # smaller LLMs
    def wrap_prompt(self, prompt: str) -> str:
        raise NotImplementedError

    def _create_auto_prompt_message(self, message: str) -> List[dict]:
        return [
            {"role": "system", "content": self.AP_SYSTEM_MESSAGE},
            {"role": "user", "content": message + "\n" + self.AP_INSTRUCTION},
        ]

    def auto_prompt(self, **kwargs) -> str:
        os.makedirs(self.folder + "/prompts", exist_ok=True)

        # if we have already done auto-prompting, just return the best prompt
        if os.path.exists(self.folder + "/prompts/best_prompt.txt"):
            with open(self.folder + "/prompts/best_prompt.txt", "r") as f:
                return f.read()

        message = kwargs["message"]
        # first run with temperature 0.0 to get the first prompt
        config = create_config(
            {},
            self._create_auto_prompt_message(message),
            max_tokens=500,
            temperature=0.0,
            model="gpt-4",
        )
        response = request_engine(config)
        greedy_prompt = self.wrap_prompt(response["choices"][0]["message"]["content"])
        with open(self.folder + "/prompts/greedy_prompt.txt", "w") as f:
            f.write(greedy_prompt)
        # repeated runs with temperature 1 to get additional prompts
        # choose the prompt with max score
        best_prompt, best_score = greedy_prompt, self.validate_prompt(greedy_prompt)
        # for i in track(range(10), description="Generating prompts..."):
        #     config = create_config({}, [message], max_tokens=500, temperature=1.0, model="gpt-4")
        #     response = request_engine(config)
        #     prompt = response["choices"][0]["message"]["content"]
        #     with open(self.folder + "/prompts/prompt_{}.txt".format(i), "w") as f:
        #         f.write(prompt)
        #     score = self.validate_prompt(prompt)
        #     if score > best_score:
        #         best_score = score
        #         best_prompt = prompt
        #     # dump score
        #     with open(self.folder + "/prompts/score_{}.txt".format(i), "w") as f:
        #         f.write(str(score))

        # dump best prompt
        with open(self.folder + "/prompts/best_prompt.txt", "w") as f:
            f.write(best_prompt)

        return best_prompt

    # initialize through either some templates or auto-prompting to determine prompts
    def initialize(self):
        self.m_logger.logo(
            "Initializing ... this may take a while ...", level=LEVEL.INFO
        )
        self.initial_prompt = self.auto_prompt(message=self.prompt_used["docstring"])
        self.prompt = self.initial_prompt
        self.m_logger.logo("Loading model ...", level=LEVEL.INFO)
        self.model = make_model(eos=self.prompt_used["separator"])
        self.m_logger.logo("Model Loaded", level=LEVEL.INFO)
        self.m_logger.logo("Done", level=LEVEL.INFO)

    def generate_chatgpt(self) -> List[str]:
        messages = create_chatgpt_docstring_template(
            self.SYSTEM_MESSAGE,
            self.prompt_used["separator"],
            self.prompt_used["docstring"],
            self.prompt_used["example_code"],
            "",
        )
        config = create_config(
            prev={}, messages=messages, max_tokens=512, temperature=1.3
        )
        ret = request_engine(config)
        func = comment_remover(simple_parse(ret["choices"][0]["message"]["content"]))
        return [func]

    def generate_model(self) -> List[str]:
        self.g_logger.logo(self.prompt, level=LEVEL.VERBOSE)
        return self.model.generate(
            self.prompt,
            batch_size=self.batch_size,
            temperature=self.temperature,
            max_length=1024,
        )

    # generation
    def generate(self, **kwargs) -> Union[List[str], bool]:
        raise NotImplementedError

    # helper for updating
    def filter(self, code: str) -> bool:
        raise NotImplementedError

    def clean_code(self, code: str) -> str:
        raise NotImplementedError

    # update
    def update(self, **kwargs):
        new_code = ""
        for result, code in kwargs["prev"]:
            if result == FResult.SAFE and self.filter(code):
                new_code = self.clean_code(code)
        if new_code != "":
            self.prompt = (
                self.initial_prompt
                + "\n"
                + new_code
                + "\n"
                + self.prompt_used["separator"]
                + "\n"
                + self.prompt_used["begin"]
            )

    # validation
    def validate_individual(self, filename) -> (FResult, str):
        raise NotImplementedError

    def parse_validation_message(self, f_result, message, file_name):
        # TODO: rewrite to include only status in TRACE but full message in VERBOSE
        self.v_logger.logo("Validating {} ...".format(file_name), LEVEL.TRACE)
        if f_result == FResult.SAFE:
            self.v_logger.logo("{} is safe".format(file_name), LEVEL.VERBOSE)
        elif f_result == FResult.FAILURE:
            self.v_logger.logo(
                "{} failed validation with error message: {}".format(
                    file_name, message, LEVEL.VERBOSE
                )
            )
        elif f_result == FResult.ERROR:
            self.v_logger.logo(
                "{} has potential error!\nerror message:\n{}".format(
                    file_name, message, LEVEL.VERBOSE
                )
            )
            self.m_logger.logo(
                "{} has potential error!".format(file_name, message, LEVEL.INFO)
            )
        elif f_result == FResult.TIMED_OUT:
            self.v_logger.logo("{} timed out".format(file_name), LEVEL.VERBOSE)

    def validate_all(self):
        for fuzz_output in track(
            glob.glob(self.folder + "/*.fuzz"),
            description="Validating",
        ):
            f_result, message = self.validate_individual(fuzz_output)
            self.parse_validation_message(f_result, message, fuzz_output)
