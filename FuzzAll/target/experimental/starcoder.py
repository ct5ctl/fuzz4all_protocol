import argparse
import json
import os
import time
from math import ceil
from pathlib import Path

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/JawTitan/huggingface/")
HF_CACHE_DIR = "/JawTitan/huggingface/hub"

EOF_STRINGS = ["<|endoftext|>", "###", "__output__ =", "if __name__"]


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
    def __init__(self, device="cuda", max_length=3000) -> None:
        checkpoint = "bigcode/starcoderbase"

        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint, cache_dir=HF_CACHE_DIR, use_auth_token=True
        )
        self.model = (
            AutoModelForCausalLM.from_pretrained(
                checkpoint,
                cache_dir=HF_CACHE_DIR,
                trust_remote_code=True,
                use_auth_token=True,
            )
            .to(torch.bfloat16)
            .to(device)
        )
        # self.eos = [self.tokenizer.encode(s)[0] for s in EOF_STRINGS]
        self.eos = EOF_STRINGS
        self.max_length = max_length
        self.prefix_token = "<fim_prefix>"
        self.suffix_token = "<fim_suffix><fim_middle>"
        self.skip_special_tokens = False

    def generate(self, prompt, batch_size=10, temperature=1.0, max_length=512):
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


_Model = StarCoder(device="cuda")

input = """
We want to target the std::span class, here are the documentation of the std::span class:
`std::span`
Description:
```
template<
    class T,
    std::size_t Extent = std::dynamic_extent
> class span;
```
The class template span describes an object that can refer to a contiguous sequence of objects with the first element of the sequence at position zero. A span can either have a static extent, in which case the number of elements in the sequence is known at compile-time and encoded in the type, or a dynamic extent.
If a span has dynamic extent, a typical implementation holds two members: a pointer to T and a size. A span with static extent may have only one member: a pointer to T.

Member functions:
begin | returns an iterator to the beginning
end | returns an iterator to the end
first | obtains a subspan consisting of the first N elements of the sequence
last | obtains a subspan consisting of the last N elements of the sequence
subspan | obtains a subspan

Please create a very short program which combines std::span with new C++ features in a complex way
#include <span>
"""

s = _Model.generate(input, temperature=1, batch_size=1)
for k in s:
    print(k)
