import argparse
import os
import subprocess

CSMITH = "/home/steven/csmith/build/bin/csmith"

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def generate(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        for num in p.track(range(args.num)):
            subprocess.run(
                f"{CSMITH} --lang-cpp --cpp11 -o {args.folder}/{num}.fuzz",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                text=True,
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--num", type=int, required=True)
    args = parser.parse_args()
    os.makedirs(args.folder, exist_ok=True)
    generate(args)


if __name__ == "__main__":
    main()
