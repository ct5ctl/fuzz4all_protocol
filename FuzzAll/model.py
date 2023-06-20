import os
from pathlib import Path
from typing import List

import torch
from dotenv import load_dotenv
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

# OPTION 1 - TRADITIONAL SETUP
# note that for using StarCoder, you need to accept the license agreement from
# the hugging face website.
# the .env file contains:
# HUGGING_FACE_HUB_TOKEN=your-token-here

dotenv_path = Path("../.env")
load_dotenv(dotenv_path=dotenv_path)
AUTH_TOKEN = os.environ.get("HUGGING_FACE_HUB_TOKEN", None)
EXEC_MODE = os.environ.get("FUZZ_EXEC_MODE", "cuda")

# OPTION 2 - SPECIFIC MODEL FOLDER SETUP
# os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/JawTitan/huggingface/")
# HF_CACHE_DIR = "/JawTitan/huggingface/hub"

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # disable warning
EOF_STRINGS = ["<|endoftext|>", "###"]


class EndOfFunctionCriteria(StoppingCriteria):
    def __init__(self, start_length, eos, tokenizer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_length = start_length
        self.eos = eos
        self.tokenizer = tokenizer
        self.end_length = {}

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if all generated sequences contain any of the end-of-function strings."""
        decoded_generations = self.tokenizer.batch_decode(
            input_ids[:, self.start_length :]
        )
        done = []
        for index, decoded_generation in enumerate(decoded_generations):
            finished = any(
                [stop_string in decoded_generation for stop_string in self.eos]
            )
            if (
                finished and index not in self.end_length
            ):  # ensures first time we see it
                for stop_string in self.eos:
                    if stop_string in decoded_generation:
                        self.end_length[index] = len(
                            input_ids[
                                index,  # get length of actual generation
                                self.start_length : -len(
                                    self.tokenizer.encode(
                                        stop_string,
                                        add_special_tokens=False,
                                        return_tensors="pt",
                                    )[0]
                                ),
                            ]
                        )
            done.append(finished)
        return all(done)


class StarCoder:
    def __init__(
        self, device: str = EXEC_MODE, eos: List = None, max_length=3000
    ) -> None:
        # checkpoint = "bigcode/starcoderbase"
        # the smaller model is easier for debugging
        checkpoint = "bigcode/tiny_starcoder_py"
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint,
            use_auth_token=AUTH_TOKEN,  # OPTION 1
            # cache_dir=HF_CACHE_DIR  # OPTION 2
        )
        self.model = (
            AutoModelForCausalLM.from_pretrained(
                checkpoint,
                use_auth_token=AUTH_TOKEN,  # OPTION 1
                # cache_dir=HF_CACHE_DIR  # OPTION 2
            )
            .to(torch.bfloat16)
            .to(device)
        )
        self.eos = EOF_STRINGS + eos
        self.max_length = max_length
        self.prefix_token = "<fim_prefix>"
        self.suffix_token = "<fim_suffix><fim_middle>"
        self.skip_special_tokens = False

    def generate(
        self, prompt, batch_size=10, temperature=1.0, max_length=512
    ) -> List[str]:
        input_str = self.prefix_token + prompt + self.suffix_token
        input_tokens = self.tokenizer.encode(input_str, return_tensors="pt").to(
            self.device
        )

        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )

        raw_outputs = self.model.generate(
            input_tokens,
            max_length=min(self.max_length, len(input_tokens[0]) + max_length),
            do_sample=True,
            top_p=1.0,
            temperature=max(temperature, 1e-2),
            num_return_sequences=batch_size,
            stopping_criteria=scores,
            output_scores=True,
            return_dict_in_generate=True,
            repetition_penalty=1.0,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


class CodeGen2:
    def __init__(
        self, device: str = EXEC_MODE, eos: List = None, max_length=3000
    ) -> None:
        checkpoint = "Salesforce/codegen2-7B"
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint,
            use_auth_token=AUTH_TOKEN,
            # cache_dir=HF_CACHE_DIR
        )
        self.model = (
            AutoModelForCausalLM.from_pretrained(
                checkpoint,
                use_auth_token=AUTH_TOKEN,
                # cache_dir=HF_CACHE_DIR
            )
            .to(torch.bfloat16)
            .to(device)
        )
        self.eos = EOF_STRINGS + eos
        self.max_length = max_length
        self.skip_special_tokens = False

    def _construct_prompt(self, prompt):
        # return prefix + "<mask_1>" + suffix + "<|endoftext|>" + "<sep>" + "<mask_1>"
        return prompt + "<mask_1>" + "<|endoftext|>" + "<sep>" + "<mask_1>"

    def generate(
        self, prompt, batch_size=10, temperature=1.0, max_length=512
    ) -> List[str]:
        input_str = self._construct_prompt(prompt)
        input_tokens = self.tokenizer.encode(input_str, return_tensors="pt").to(
            self.device
        )

        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )

        raw_outputs = self.model.generate(
            input_tokens,
            max_length=min(self.max_length, len(input_tokens[0]) + max_length),
            do_sample=True,
            top_p=1.0,
            temperature=max(temperature, 1e-2),
            num_return_sequences=batch_size,
            stopping_criteria=scores,
            output_scores=True,
            return_dict_in_generate=True,
            repetition_penalty=1.0,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


def make_model(eos: List = None):
    return StarCoder(eos=eos)
    # return CodeGen2(eos=eos)
