import argparse
import openai
import os
import subprocess
import time

from util.api_request import create_openai_config, request_engine
from util.util import comment_remover
from target.base_target import Target
from template import C_TEMPLATE, FIRST, SECOND, THIRD
# cpp 23
from template import CPP_TEMPLATE_consteval, CPP_TEMPLATE_multi_dimen_access, CPP_TEMPLATE_auto_functional
# cpp 20
from template import CPP_TEMPLATE_coroutines, CPP_TEMPLATE_likely_unlikely, CPP_TEMPLATE_immediate_function

CURRENT_TIME = time.time()


def generation(args):
    with open(args.folder + "/prompt.txt", "w") as f:
        f.write(C_TEMPLATE)
    config = create_openai_config(CPP_TEMPLATE_auto_functional,
                                  stop=['// create a fuzzing testcase for a C++ compiler for feature "auto in functional-style cast"'],
                                  n=5,
                                  temperature=1,
                                  max_tokens=500)

    index = 0
    for i in range(0, 3000):
        ret = request_engine(config)
        for choice in ret:
            if choice['finish_reason'] == 'length':  # did not hit stop
                continue
            print("========== sample =========")
            print(choice['text'])
            with open(args.folder + "/{}.{}".format(index, args.language), "w") as f:
                f.write(choice['text'])
            index += 1


def _create_fifo_template(separator, first, second, third):
    if third == "":
        return (separator + "\n").join(["", first + "\n\n", second + "\n\n", "\n"])
    return (separator+"\n").join(["", first+"\n\n", second+"\n\n", third+"\n\n", "\n"])


def generation_fifo(args):
    with open(args.folder + "/prompt.txt", "w") as f:
        f.write(C_TEMPLATE)

    prompt_used = CPP_TEMPLATE_immediate_function

    index = 0
    first, second, third = prompt_used['first'].strip(), prompt_used['second'].strip(), prompt_used['third'].strip()
    for i in range(0, 5000):
        print(_create_fifo_template(prompt_used['separator'], first, second, third))
        config = create_openai_config(_create_fifo_template(prompt_used['separator'], first, second, third),
                                      stop=[prompt_used['separator']],
                                      n=5,
                                      temperature=1,
                                      max_tokens=500)
        ret = request_engine(config)
        for choice in ret:
            if choice['finish_reason'] == 'length' \
                    or len(comment_remover(choice['text'].strip())) < 100:  # did not hit stop
                print("------------- length reason ----------- ")
                print(choice['text'])
                print("------------- length reason ----------- ")
                continue
            print("========== sample =========")
            print(choice['text'])
            print("========== sample =========")
            with open(args.folder + "/{}.{}".format(index, args.language), "w") as f:
                f.write(choice['text'])
            index += 1
            if _check_syntax_valid(choice['text']):
                if third != "":
                    first = second
                    second = third
                third = choice['text'].strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--key_file", type=str, default="api_key.txt")
    parser.add_argument("--language", type=str, default="c")
    args = parser.parse_args()
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    openai.api_key = open(args.key_file, 'r').read().strip()

    generation_fifo(args)


if __name__ == "__main__":
    main()
