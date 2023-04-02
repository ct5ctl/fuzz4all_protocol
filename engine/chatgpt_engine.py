import argparse
import openai
import os


def generation_fifo(args):
    pass


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
