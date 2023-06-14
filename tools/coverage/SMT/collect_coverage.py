import argparse
import glob
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


def clean_coverage(args):
    subprocess.run(
        f"cd {args.smt_folder}; make coverage-reset",
        shell=True,
        encoding="utf-8",
    )


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


def run_smt(smt_engine: str, source: str, pre_flags: str, post_flags: str):
    try:
        exit_code = subprocess.run(
            f"{smt_engine} {pre_flags} {source} {post_flags}",
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=5,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
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


def coverage_loop(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        # clean coverage
        clean_coverage(args)

        # loop through all files in folder in alphanumeric order
        files = glob.glob(args.folder + "/*.fuzz")
        files.sort(key=natural_sort_key)
        index = 0
        for file in p.track(files):
            run_smt(args.smt, file, "-m -i -q --check-models --lang smt2", "")
            if (index + 1) % int(args.interval) == 0:
                line_cov, func_cov = get_coverage(args)
                with open(args.folder + "/coverage.csv", "a") as f:
                    f.write(f"{index + 1},{line_cov},{func_cov}\n")
            index += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smt", type=str, required=True)
    parser.add_argument("--smt_folder", type=str, required=True)
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--interval", type=str, required=True)
    args = parser.parse_args()

    coverage_loop(args)


if __name__ == "__main__":
    main()
