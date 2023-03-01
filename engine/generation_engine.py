import argparse
import openai
import os
import subprocess

from util.api_request import create_openai_config, request_engine
from target.base_target import Target
from template import C_TEMPLATE, FIRST, SECOND, THIRD


def generation(args):
    with open(args.folder + "/prompt.txt", "w") as f:
        f.write(C_TEMPLATE)
    config = create_openai_config(C_TEMPLATE,
                                  stop=["// create a fuzzing testcase for a C compiler"],
                                  n=5,
                                  temperature=1,
                                  max_tokens=500)

    index = 0
    for i in range(0, 1000):
        ret = request_engine(config)
        for choice in ret:
            if choice['finish_reason'] == 'length':  # did not hit stop
                continue
            print("========== sample =========")
            print(choice['text'])
            with open(args.folder + "/{}.c".format(index), "w") as f:
                f.write(choice['text'])
            index += 1


def _create_fifo_template(first, second, third):
    return "// create a fuzzing testcase for a C compiler\n".join(["", first+"\n\n", second+"\n\n", third+"\n\n", "\n"])


def _check_syntax_valid(code):
    with open("temp.c", "w") as f:
        f.write(code)
    exit_code = subprocess.run("gcc -c -fsyntax-only {}".format("temp.c"), shell=True, capture_output=True, text=True)
    if exit_code.returncode == 0:
        return True
    else:
        return False


def generation_fifo(args):
    with open(args.folder + "/prompt.txt", "w") as f:
        f.write(C_TEMPLATE)

    index = 0
    first, second, third = FIRST.strip(), SECOND.strip(), THIRD.strip()
    for i in range(0, 5000):
        print(_create_fifo_template(first, second, third))
        config = create_openai_config(_create_fifo_template(first, second, third),
                                      stop=["// create a fuzzing testcase for a C compiler"],
                                      n=5,
                                      temperature=1,
                                      max_tokens=500)
        ret = request_engine(config)
        for choice in ret:
            if choice['finish_reason'] == 'length' or len(choice['text'].strip()) < 100:  # did not hit stop
                continue
            print("========== sample =========")
            print(choice['text'])
            with open(args.folder + "/{}.c".format(index), "w") as f:
                f.write(choice['text'])
            index += 1
            if _check_syntax_valid(choice['text']):
                first = second
                second = third
                third = choice['text'].strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--key_file", type=str, default="api_key.txt")
    args = parser.parse_args()
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    openai.api_key = open(args.key_file, 'r').read().strip()

    generation_fifo(args)


if __name__ == "__main__":
    main()