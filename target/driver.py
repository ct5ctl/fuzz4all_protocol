import argparse

from target.CPP.GPP12 import GPP12Target
from target.SMT.SMT import SMTTarget


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--target", type=str, default="gpp12")
    args = parser.parse_args()

    if args.target == "gpp12":
        target = GPP12Target(language="cpp", timeout=10, folder=args.folder)
    elif args.target == "smt":
        target = SMTTarget(language="smt2", timeout=10, folder=args.folder)
    else:
        raise NotImplementedError

    target.validate_all()


if __name__ == "__main__":
    main()
