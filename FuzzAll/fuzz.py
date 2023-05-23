import argparse
import os


def fuzz(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--language", type=str, default="c")
    args = parser.parse_args()

    assert not os.path.exists(args.folder), f"{args.folder} already exists!"
    os.makedirs(args.folder)

    fuzz(args)


if __name__ == "__main__":
    main()
