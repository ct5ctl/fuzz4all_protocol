import argparse
import glob
import os
import subprocess
import time

from rich.traceback import install

from FuzzAll.util.util import natural_sort_key

install()
CURRENT_TIME = time.time()

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def run_smt(smt_engine: str, source: str, pre_flags: str, post_flags: str):
    try:
        exit_code = subprocess.run(
            f"{smt_engine} {pre_flags} {source} {post_flags}",
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=1,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
        print(source)
        pname = f"'{source}'"
        subprocess.run(
            ["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"],
            shell=True,
        )
        subprocess.run(
            [
                "ps -ef | grep "
                + pname
                + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"
            ],
            shell=True,
        )  # kill all tests thank you


def clean_coverage(args):
    subprocess.run(
        f"cd {args.smt_folder}; make coverage-reset",
        shell=True,
        encoding="utf-8",
    )


def run_typefuzz(args):
    start_time = time.time()
    # continue until 24 hours
    while time.time() - start_time < 24 * 60 * 60:
        # run typefuzz
        timeout = int(24 * 60 * 60 - (time.time() - start_time))
        subprocess.run(
            f'cd /home/steven/yinyang; timeout {timeout}s typefuzz --keep-mutants -s {args.folder} "z3 model_validate=true;cvc5 -m -i -q --check-models" seeds',
            shell=True,
            encoding="utf-8",
            text=True,
            capture_output=True,
        )
        print("Restarted ... ")


def get_coverage(args):
    exit_code = subprocess.run(
        f"cd {args.smt_folder}; make coverage",
        shell=True,
        encoding="utf-8",
        text=True,
        capture_output=True,
    )
    line_cov, func_cov = 0, 0
    for line in exit_code.stdout.splitlines():
        if line.strip().startswith("lines......:"):
            line_cov = int(line.strip().split("(")[1].split(" ")[0])
        elif line.strip().startswith("functions..:"):
            func_cov = int(line.strip().split("(")[1].split(" ")[0])
    print(line_cov, func_cov)
    return line_cov, func_cov


def coverage_seeds(args):
    clean_coverage(args)
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        for filename in p.track(glob.glob(f"{args.folder}/**/*.smt2", recursive=True)):
            run_smt(args.smt, filename, "-m -i -q --check-models --lang smt2", "")

    line_cov, func_cov = get_coverage(args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--seeds", action="store_true")
    parser.add_argument("--run", action="store_true")

    parser.add_argument("--smt", type=str, required=True)
    parser.add_argument("--smt_folder", type=str, required=True)

    args = parser.parse_args()

    if args.seeds:
        # computer seed coverage
        coverage_seeds(args)
    elif args.run:
        run_typefuzz(args)


if __name__ == "__main__":
    main()
