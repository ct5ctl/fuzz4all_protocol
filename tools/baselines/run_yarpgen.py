import argparse
import glob
import os
import subprocess
import time

YARPGEN = "/home/steven/yarpgen/yarpgen"

from rich.traceback import install

install()

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from FuzzAll.util.util import natural_sort_key

CURRENT_TIME = time.time()


def generate(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        for num in p.track(range(15000, args.num)):
            os.makedirs(f"{args.folder}/{num}", exist_ok=True)
            subprocess.run(
                f"{YARPGEN} --std=c++17 -d {args.folder}/{num}",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                text=True,
            )


def clean_coverage(args):
    subprocess.run(
        f"cd {args.cov_folder}; lcov --zerocounters --directory .",
        shell=True,
        encoding="utf-8",
    )


def run_compile(
    folder: str, compiler: str, source: str, pre_flags: str, post_flags: str
):
    try:
        # print(f"cd {folder} && {compiler} {pre_flags} {source} {post_flags}")
        exit_code = subprocess.run(
            f"cd {folder} &&" f"{compiler} {pre_flags} {source} {post_flags}",
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=10,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
        print(f"cd {folder} && {compiler} {pre_flags} {source} {post_flags}")
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

    return


def get_coverage(args):
    subprocess.run(
        f"cd {args.cov_folder}; lcov --capture --directory . --output-file coverage.info --gcov-tool {args.gcov}",
        shell=True,
        encoding="utf-8",
        text=True,
        capture_output=True,
    )
    exit_code = subprocess.run(
        f"cd {args.cov_folder}; lcov --summary coverage.info",
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


def coverage(args):
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
        folders = glob.glob(args.folder + "/*/")
        folders.sort(key=natural_sort_key)
        index = 0
        for folder in p.track(folders):

            # skip until start
            if index + 1 < args.start:
                index += 1
                continue

            # compile the file
            run_compile(
                folder,
                args.compiler,
                "driver.cpp func.cpp",
                f"-x c++ -std=c++23",
                f"-o /tmp/out{CURRENT_TIME}",
            )
            if (index + 1) % args.interval == 0 and index + 1 >= args.start:
                # get the coverage
                line_cov, func_cov = get_coverage(args)
                # append to csv file
                with open(args.folder + "/coverage.csv", "a") as f:
                    f.write(f"{index + 1},{line_cov},{func_cov}\n")

            if index + 1 >= args.end:
                break
            index += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--num", type=int, required=True)
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--interval", type=int)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=1000000000)
    parser.add_argument("--cov_folder", type=str)
    parser.add_argument("--gcov", type=str)
    parser.add_argument("--compiler", type=str)
    args = parser.parse_args()
    if args.coverage:
        coverage(args)
    else:
        os.makedirs(args.folder, exist_ok=True)
        generate(args)


if __name__ == "__main__":
    main()
