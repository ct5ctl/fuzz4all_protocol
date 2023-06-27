import argparse
import os

from rich.traceback import install

install()

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
        task = p.add_task("Fuzzing", total=args.num)
        count = 0

        if args.resume:
            n_existing = [
                int(f.split(".")[0])
                for f in os.listdir(args.folder)
                if f.endswith(".fuzz")
            ]
            n_existing.sort(reverse=True)
            if len(n_existing) > 0:
                count = n_existing[0] + 1
            log = f" (resuming from {count})"
            p.console.print(log)

        p.update(task, advance=count)

        while count < args.num:
            fos = target.generate()
            if not fos:
                target.initialize()
                continue
            prev = []
            for index, fo in enumerate(fos):
                file_name = os.path.join(args.folder, f"{count}.fuzz")
                write_to_file(fo, file_name)
                count += 1
                p.update(task, advance=1)
                # validation on the fly
                if args.otf:
                    f_result, message = target.validate_individual(file_name)
                    target.parse_validation_message(f_result, message, file_name)
                    prev.append((f_result, fo))
            target.update(prev=prev)


# evaluate against the oracle to discover any potential bugs
# used after the generation
def evaluate(args, target: Target):
    target.validate_all()


def main():
    """Main function to start the fuzzing process.

    Remember that make_target uses these arguments:

    An example command to run this script on cpp:
    ```bash
    python fuzz.py \
    --language cpp --num 10 --otf --level 3 \
    --template cpp_expected \
    --bs 1 --temperature 1.0 --prompt_strategy 0 --use_hw
    ```
    """
    parser = argparse.ArgumentParser()
    # basic options, individual language/target options are referenced in make_target
    parser.add_argument(
        "--folder", type=str, default="Results/test", help="folder to store results"
    )
    parser.add_argument(
        "--language",
        type=str,
        required=True,
        help="""
            language to fuzz, currently supported: cpp, smt2, java, go
        """,
    )
    parser.add_argument("--num", type=int, required=True)
    parser.add_argument(
        "--level",
        type=int,
        required=True,
        help="""
            level of logging: 1 = INFO, 2 = TRACE, 3 = VERBOSE
        """,
    )
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--otf",
        action="store_true",
        help="use to validate fuzzing outputs on the fly. If flag not "
        "set then only generation will be done",
    )

    args = parser.parse_known_args()[0]
    args, target = make_target(args, parser)
    if not args.evaluate:
        assert (
            not os.path.exists(args.folder) or args.resume
        ), f"{args.folder} already exists!"
        os.makedirs(args.folder, exist_ok=True)
        fuzz(args, target)
    else:
        evaluate(args, target)


if __name__ == "__main__":
    main()
