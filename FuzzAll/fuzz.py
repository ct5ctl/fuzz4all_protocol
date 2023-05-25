import argparse
import os

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from FuzzAll.make_target import make_target
from FuzzAll.target.target import Target


def write_to_file(fo, file_name):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(fo)
    except:
        pass


def fuzz(args, target: Target):
    target.initialize()
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        count = 0
        for i in p.track(range(args.num)):
            fos = target.generate()
            for index, fo in enumerate(fos):
                file_name = os.path.join(args.folder, f"{count}.fuzz")
                write_to_file(fo, file_name)
                count += 1
                # validation on the fly
                if args.otf:
                    f_result, message = target.validate_individual(file_name)
                    print(f_result, message)
                    target.parse_validation_message(f_result, message, file_name)


# evaluate against the oracle to discover any potential bugs
# used after the generation
def evaluate(args, target: Target):
    target.validate_all()


def main():
    # TODO: set restart option
    parser = argparse.ArgumentParser()
    # basic options, individual language/target options are referenced in make_target
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--language", type=str, required=True)
    parser.add_argument("--num", type=int, required=True)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument(
        "--otf",
        action="store_true",
        help="use to validate fuzzing outputs on the fly. If flag not "
        "set then only generation will be done",
    )

    args = parser.parse_known_args()[0]
    args, target = make_target(args, parser)
    if not args.evaluate:
        # assert not os.path.exists(args.folder), f"{args.folder} already exists!"
        os.makedirs(args.folder, exist_ok=True)
        fuzz(args, target)
    else:
        evaluate(args, target)


if __name__ == "__main__":
    main()
