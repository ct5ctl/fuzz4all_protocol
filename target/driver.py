import argparse

from GCC import GCCTarget


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--target", type=str, default="gcc")
    args = parser.parse_args()

    target = GCCTarget("c", folder=args.folder)
    target.validate_all()


if __name__ == "__main__":
    main()