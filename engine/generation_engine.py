import argparse
import openai
import os

from util.api_request import create_openai_config, request_engine
from target.base_target import Target
from template import C_TEMPLATE


def generation(args):
    config = create_openai_config(C_TEMPLATE,
                                  stop=["// create a random C file"],
                                  n=5,
                                  temperature=1,
                                  max_tokens=500)
    for i in range(0, 100):
        ret = request_engine(config)
        for choice in ret:
            if choice['finish_reason'] == 'length':  # did not hit stop
                continue
            print("========== sample =========")
            print(choice['text'])
            with open(args.folder + "/{}.c".format(i), "w") as f:
                f.write(choice['text'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--key_file", type=str, default="api_key.txt")
    args = parser.parse_args()
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    openai.api_key = open(args.key_file, 'r').read().strip()

    generation(args)


if __name__ == "__main__":
    main()