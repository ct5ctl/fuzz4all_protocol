# note the actual running of grayc is done through docker image
# provided by the grayc artifact
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


def clean_coverage(args):
    subprocess.run(
        f"cd {args.cov_folder}; lcov --zerocounters --directory .",
        shell=True,
        encoding="utf-8",
    )


def run_compile(compiler: str, source: str, pre_flags: str, post_flags: str):
    try:
        exit_code = subprocess.run(
            f"{compiler} {pre_flags} {source} {post_flags}",
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

    return


def save_coverage(args):
    # create folder for coverage
    if os.path.exists(args.folder + "/prev_coverage"):
        subprocess.run(
            f"cd {args.folder}; rm -rf prev_coverage",
            shell=True,
            encoding="utf-8",
        )
    os.makedirs(args.folder + "/prev_coverage", exist_ok=True)
    # copy coverage folder to fuzzing folder
    subprocess.run(
        "cd "
        + args.cov_folder
        + '; find -type f -name "*.gcda" -exec cp --parent {} '
        + args.folder
        + "/prev_coverage \;",
        shell=True,
        encoding="utf-8",
    )
    print("Coverage saved")


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


def coverage_seeds(args):
    # clean coverage
    clean_coverage(args)

    files = glob.glob(args.seed_folder + "/*/*.c")
    for file in files:
        # compile the file
        run_compile(
            args.compiler,
            file,
            f"-x c++ -std=c++23",
            f"-o /tmp/out{CURRENT_TIME}",
        )

    line_cov, func_cov = get_coverage(args)
    # save_coverage(args)
    # seed coverage: 187051 21667
    return line_cov, func_cov


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
        line_cov, func_cov = coverage_seeds(args)
        with open(args.folder + "/coverage.csv", "a") as f:
            f.write(f"{0},{line_cov},{func_cov},{0}\n")

        files = glob.glob(args.folder + "/*.c")
        files.sort(key=natural_sort_key)
        initial_time = "-".join(
            files[0].split("fuzzer-file-")[-1].split("-")[1:]
        ).split(".")[0]
        print(initial_time)
        # convert string to time
        initial_time = time.mktime(time.strptime(initial_time, "%Y-%m-%d-%H:%M:%S"))
        start_time = initial_time

        for file in p.track(files):
            run_compile(
                args.compiler,
                file,
                f"-x c++ -std=c++23 ",
                f"-o /tmp/out{CURRENT_TIME}",
            )
            file_time = "-".join(file.split("fuzzer-file-")[-1].split("-")[1:]).split(
                "."
            )[0]
            file_time = time.mktime(time.strptime(file_time, "%Y-%m-%d-%H:%M:%S"))
            time_seconds = file_time - start_time
            if time_seconds >= 60 * 20:
                line_cov, func_cov = get_coverage(args)
                with open(args.folder + "/coverage.csv", "a") as f:
                    f.write(
                        f"{0},{line_cov},{func_cov},{os.path.getmtime(file) - initial_time}\n"
                    )
                start_time = file_time

        line_cov, func_cov = get_coverage(args)
        with open(args.folder + "/coverage.csv", "a") as f:
            f.write(f"{0},{line_cov},{func_cov},{24 * 60 * 60}\n")
        save_coverage(args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--seed_folder", type=str)
    parser.add_argument("--seeds", action="store_true")
    parser.add_argument("--cov_folder", type=str)
    parser.add_argument("--gcov", type=str)
    parser.add_argument("--compiler", type=str)
    args = parser.parse_args()
    if args.seeds:
        # compute seed coverage
        coverage_seeds(args)
    else:
        coverage_loop(args)


if __name__ == "__main__":
    main()
