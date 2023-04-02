import argparse

from GCC import GCCTarget
from GPP12 import GPP12Target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--target", type=str, default="gcc")
    args = parser.parse_args()

    if args.target == "gcc":
        target = GCCTarget("c", folder=args.folder)
    elif args.target == "gpp12":
        target = GPP12Target("cpp", folder=args.folder)
    else:
        raise NotImplementedError

    target.validate_all()


if __name__ == "__main__":
    main()
