import argparse
import glob
import os
import subprocess

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

        with open("go-fuzz-std-corpus", "r") as f:
            targets = f.readlines()

        print(f"{args.timelimit * 3600 / len(targets)} seconds per target")

        for target in p.track(targets):
            print(target.strip().split("/")[-2])

            x = target.strip().split("/")[-2]
            if x == "suffixrray":
                x = "suffix"
            try:
                subprocess.run(
                    f'export PATH="$(~/sdk/go1.17/bin/go env GOROOT)"/bin:"$PATH" && cd {target.strip()}/.. '
                    f"&& go-fuzz -bin={x}-fuzz.zip -func Fuzz",
                    shell=True,
                    capture_output=True,
                    encoding="utf-8",
                    text=True,
                    timeout=args.timelimit * 3600 / len(targets),
                )
            except subprocess.TimeoutExpired:
                continue

            assert False, "go-fuzz failed"


def build(args):
    for x in glob.glob(args.folder + "/*/corpus"):
        exit_code = subprocess.run(
            f'export PATH="$(~/sdk/go1.17/bin/go env GOROOT)"/bin:"$PATH" && cd {x} && cd .. && go-fuzz-build .',
            shell=True,
            capture_output=True,
            encoding="utf-8",
            text=True,
        )
        if exit_code.returncode == 0:
            print(x)


# collects coverage
# involves modifying the existing file to read from basically the corpus folder
# and then computing the coverage on the go standard library.
def coverage(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        with open("go-fuzz-std-corpus", "r") as f:
            targets = f.readlines()

        # prev_cov = {}

        import json

        with open(
            "/home/steven/FuzzAll/tools/go-fuzz-coverage-seed/prev_coverage.json", "r"
        ) as f:
            prev_cov = json.load(f)

        index = 0

        for target in p.track(targets):
            print(target.strip().split("/")[-2])

            x = target.strip().split("/")[-2]
            files = glob.glob(
                target.replace("go-fuzz-corpus-real", "go-fuzz-corpus").strip()
                + "/../*.go"
            )

            #             with open(files[0], "r") as f:
            #                 content = f.read()
            #
            #             # replace original package name with main
            #             import regex
            #             x = regex.findall(r"package (.*)", content)[0]
            #             content = content.replace("package " + x, "package main")
            #
            #             code = content.split("func Fuzz")
            #
            #             import_code = """
            # import (
            #     "flag"
            #     "io/ioutil"
            # )
            #             """
            #
            #             if x == "flate" or x == "mail" or x == "zlib" or x == "gzip" or x == "htmltemplate" or x == "httpreq" or x == "tar" or x == "lzw" or x == "bzip2" or x == "goast":
            #                 import_code = """
            # import (
            #     "flag"
            # )
            #             """
            #             if x == "flag":
            #                 import_code = """
            # import (
            #     "io/ioutil"
            # )
            #                             """
            #
            #
            #             main_code = """
            # func main() {
            #     wordPtr := flag.String("file", "tmp", "a string")
            #     flag.Parse()
            #     v, _ := ioutil.ReadFile(*wordPtr)  //read the content of file
            #     Fuzz(v)
            # }
            #             """
            #
            #             content = code[0] + import_code + main_code + "\nfunc Fuzz" + code[1]
            #
            #             with open(files[0], "w") as f:
            #                 f.write(content)

            # try:
            #     exit_code = subprocess.run(
            #         f"cd {target.replace('go-fuzz-corpus-real', 'go-fuzz-corpus').strip() + '/../'} "
            #         f"&& go build -cover -o myprogram.exe -coverpkg=all . ",
            #         shell=True,
            #         encoding="utf-8",
            #         capture_output=True,
            #         timeout=5,
            #         text=True,
            #     )
            # except subprocess.TimeoutExpired as te:
            #     pname = f"'myprogram.exe'"
            #     subprocess.run(
            #         ["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"],
            #         shell=True,
            #     )
            #     subprocess.run(
            #         [
            #             "ps -ef | grep "
            #             + pname
            #             + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"
            #         ],
            #         shell=True,
            #     )  # kill all tests thank you
            #     assert False
            # except UnicodeDecodeError as ue:
            #     assert False
            #
            # print(exit_code.returncode)

            # collect coverage
            for gen_files in glob.glob(target.strip() + "/*"):
                # print(gen_files)
                if not os.path.isfile(
                    gen_files.replace("go-fuzz-corpus-real", "go-fuzz-corpus")
                ):
                    prev_cov = get_coverage(
                        target.replace("go-fuzz-corpus-real", "go-fuzz-corpus").strip()
                        + "/../",
                        gen_files,
                        prev_cov,
                    )

                # prev_cov = get_coverage(target.replace('go-fuzz-corpus-real', 'go-fuzz-corpus').strip() + '/../',
                #                         gen_files, prev_cov)

                if (index + 1) % args.interval == 0 and index + 1 >= args.interval:
                    stmt_cv = count_coverage(prev_cov)
                    with open(args.folder + "/coverage.csv", "a") as f:
                        f.write(f"{index + 1},{stmt_cv},{0}\n")

                index += 1

        import json

        with open(args.folder + "/prev_coverage.json", "w") as f:
            json.dump(prev_cov, f)


def get_coverage(target_folder, input_file, prev_cov):
    coverage_folder = "coverage"

    subprocess.run(
        f"rm -rf {target_folder}/{coverage_folder}",
        shell=True,
        encoding="utf-8",
    )

    subprocess.run(
        f"rm -rf {target_folder}/{coverage_folder}.txt",
        shell=True,
        encoding="utf-8",
    )

    os.makedirs(f"{target_folder}/{coverage_folder}", exist_ok=True)

    try:
        exit_code = subprocess.run(
            f"cd {target_folder} "
            f"&& GOCOVERDIR={coverage_folder} ./myprogram.exe -file={input_file}"
            f"&& go tool covdata debugdump -i={coverage_folder} > {coverage_folder}.txt",
            shell=True,
            encoding="utf-8",
            capture_output=True,
            timeout=1,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
        print("timeout")
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

    with open(f"{target_folder}/{coverage_folder}.txt", "r") as f:
        cov = f.read()

    covered_stmt = 0

    for cov_func in cov.split("Func: ")[1:]:
        # print(cov_func)
        func_name = cov_func.split("\n")[0].strip()
        src_file = cov_func.split("\n")[1].strip().split("Srcfile: ")[1].strip()

        if "example/" in src_file:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--interval", type=int, required=True)
    # time in hours
    parser.add_argument("--timelimit", type=float, required=True)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--coverage", action="store_true")

    args = parser.parse_args()

    if args.build:
        build(args)
    elif args.coverage:
        coverage(args)
    else:
        generate(args)


if __name__ == "__main__":
    main()
