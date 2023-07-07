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


def setup():
    # before setup there is teardown
    teardown()
    # make tmp folder
    os.makedirs(f"/tmp/coverage{CURRENT_TIME}", exist_ok=True)
    # make go mod file
    with open(f"/tmp/coverage{CURRENT_TIME}/go.mod", "w", encoding="utf-8") as f:
        f.write("module fuzzing.com\n")

    os.makedirs(f"/tmp/coverage{CURRENT_TIME}/tmp", exist_ok=True)


def teardown():
    # remove tmp folder
    subprocess.run(
        f"rm -rf /tmp/coverage{CURRENT_TIME}",
        shell=True,
        encoding="utf-8",
    )


def test_textfmt():
    with open("/home/steven/go-fuzz-corpus-real/aes/coverprofile", "r") as f:
        cov = f.read()

    covered_stmts, total_stmts = 0, 0

    for cov_func in cov.splitlines()[1:]:
        uid = cov_func.split(" ")[0]
        stmts, covered = int(cov_func.split(" ")[1]), int(cov_func.split(" ")[2])
        if covered > 0:
            covered_stmts += stmts
        total_stmts += stmts

    print(
        f"Covered: {covered_stmts}/{total_stmts} ({covered_stmts / total_stmts * 100:.2f}%)"
    )


def test():
    with open("test.txt", "r") as f:
        cov = f.read()

    covered_stmts, total_stmts = 0, 0

    for cov_func in cov.split("Func: ")[1:]:
        # print(cov_func)
        func_name = cov_func.split("\n")[0].strip()
        src_file = cov_func.split("\n")[1].strip().split("Srcfile: ")[1].strip()

        uid = f"file{src_file}:{func_name}"
        print(uid)
        for line in cov_func.split("\n")[3:]:
            # check line[0] is an digit
            if line == "" or line[0] not in "0123456789":
                continue
            stmts, covered = int(line.split("NS=")[1].strip().split(" = ")[0]), int(
                line.split("NS=")[1].strip().split(" = ")[1]
            )
            if covered == 1:
                covered_stmts += stmts
            total_stmts += stmts

    print(
        f"Covered: {covered_stmts}/{total_stmts} ({covered_stmts/total_stmts*100:.2f}%)"
    )


def get_coverage(file, prev_cov):

    setup()

    subprocess.run(
        f"cp {file} /tmp/coverage{CURRENT_TIME}/main.go",
        shell=True,
        encoding="utf-8",
    )

    # run go build with coverage and execute
    try:
        exit_code = subprocess.run(
            f"cd /tmp/coverage{CURRENT_TIME} && go build -cover -o myprogram.exe -coverpkg=all . "
            f"&& GOCOVERDIR=tmp ./myprogram.exe "
            f"&& go tool covdata debugdump -i=tmp > coverage.txt",
            shell=True,
            encoding="utf-8",
            capture_output=True,
            timeout=5,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
        pname = f"'myprogram.exe'"
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
        return prev_cov
    except UnicodeDecodeError as ue:
        return prev_cov

    if exit_code.returncode != 0:
        return prev_cov

    with open(f"/tmp/coverage{CURRENT_TIME}/coverage.txt", "r") as f:
        cov = f.read()

    covered_stmt = 0

    for cov_func in cov.split("Func: ")[1:]:
        # print(cov_func)
        func_name = cov_func.split("\n")[0].strip()
        src_file = cov_func.split("\n")[1].strip().split("Srcfile: ")[1].strip()

        if src_file == "fuzzing.com/main.go":
            continue

        uid = f"file{src_file}:{func_name}"

        if uid not in prev_cov:
            prev_cov[uid] = {}

        for line in cov_func.split("\n")[3:]:
            # check line[0] is an digit
            if line == "" or line[0] not in "0123456789":
                continue
            stmts, covered = int(line.split("NS=")[1].strip().split(" = ")[0]), int(
                line.split("NS=")[1].strip().split(" = ")[1]
            )

            if line.split(":")[0] not in prev_cov[uid]:
                prev_cov[uid][line.split(":")[0]] = 0

            if covered:
                prev_cov[uid][line.split(":")[0]] = stmts
                covered_stmt += stmts

        # count_coverage(prev_cov)
    return prev_cov


def count_coverage(prev_cov):
    covered_stmts = 0
    for uid in prev_cov:
        for _, stmts in prev_cov[uid].items():
            covered_stmts += stmts
    print(covered_stmts)
    return covered_stmts


def coverage_loop(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:

        # setup
        setup()

        import json

        with open(
            "/home/steven/fastd/fuzzall/FuzzAll/experiment/go/std_library/prev_coverage.json",
            "r",
        ) as f:
            prev_coverage = json.load(f)
        # prev_coverage = {}

        # loop through all files in folder in alphanumeric order
        files = glob.glob(args.folder + "/*.fuzz")
        files.sort(key=natural_sort_key)
        index = 0
        for file in p.track(files):
            # skip until start
            if index + 1 < args.start:
                index += 1
                continue

            # compile the file
            get_coverage(file, prev_coverage)
            if index + 1 >= args.end:
                break

            if (index + 1) % args.interval == 0 and index + 1 >= args.interval:
                stmt_cv = count_coverage(prev_coverage)
                with open(args.folder + "/coverage.csv", "a") as f:
                    f.write(f"{index + 1},{stmt_cv},{0}\n")

            if index + 1 >= args.end:
                break

            index += 1

        import json

        with open(args.folder + "/prev_coverage.json", "w") as f:
            json.dump(prev_coverage, f, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=1000000000)

    args = parser.parse_args()

    coverage_loop(args)
    # test_textfmt()


if __name__ == "__main__":
    main()
