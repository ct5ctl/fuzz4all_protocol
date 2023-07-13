"""Main script to run the fuzzing process.

Usage:
1. Use with config file (from the main repo folder):
    python FuzzAll/fuzz.py --config=<config_file> main_with_config
    e.g. python FuzzAll/fuzz.py --config=config/v02_qiskit_basic.yaml main_with_config
2. Use with command line arguments (from the main repo folder):
    python FuzzAll/fuzz.py main \
    --language=cpp --num=10 --otf --level=1 \
    --template=cpp_expected \
    --bs=1 --temperature=1.0 --prompt_strategy=0 --use_hw

"""

import os
import time

import click
from rich.traceback import install

install()

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from FuzzAll.make_target import make_target, make_target_with_config
from FuzzAll.target.target import Target
from FuzzAll.util.util import load_config_file


def write_to_file(fo, file_name):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(fo)
    except:
        pass


def fuzz(
    target: Target,
    number_of_iterations: int,
    total_time: int,
    output_folder: str,
    resume: bool,
    otf: bool,
):
    target.initialize()
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        task = p.add_task("Fuzzing", total=number_of_iterations)
        count = 0
        start_time = time.time()

        if resume:
            n_existing = [
                int(f.split(".")[0])
                for f in os.listdir(output_folder)
                if f.endswith(".fuzz")
            ]
            n_existing.sort(reverse=True)
            if len(n_existing) > 0:
                count = n_existing[0] + 1
            log = f" (resuming from {count})"
            p.console.print(log)

        p.update(task, advance=count)

        while (
            count < number_of_iterations
            and time.time() - start_time < total_time * 3600
        ):
            fos = target.generate()
            if not fos:
                target.initialize()
                continue
            prev = []
            for index, fo in enumerate(fos):
                file_name = os.path.join(output_folder, f"{count}.fuzz")
                write_to_file(fo, file_name)
                count += 1
                p.update(task, advance=1)
                # validation on the fly
                if otf:
                    f_result, message = target.validate_individual(file_name)
                    target.parse_validation_message(f_result, message, file_name)
                    prev.append((f_result, fo))
            target.update(prev=prev)


# evaluate against the oracle to discover any potential bugs
# used after the generation
def evaluate(target: Target):
    target.validate_all()


@click.group()
@click.option(
    "config_file",
    "--config",
    type=str,
    default=None,
    help="Path to the configuration file.",
)
@click.pass_context
def cli(ctx, config_file):
    """Run the main using a configuration file."""
    if config_file is not None:
        config_dict = load_config_file(config_file)
        ctx.ensure_object(dict)
        ctx.obj["CONFIG_DICT"] = config_dict


@cli.command("main")
@click.option(
    "folder",
    "--folder",
    type=str,
    default="Results/test",
    help="folder to store results",
)
@click.option(
    "language",
    "--language",
    type=str,
    required=True,
    help="language to fuzz, currently supported: cpp, smt2, java, go",
)
@click.option("num", "--num", type=int, required=True, help="number of iterations")
@click.option(
    "total_time", "--total_time", type=int, required=True, help="total time in hours"
)
@click.option(
    "level",
    "--level",
    type=int,
    required=True,
    help="level of logging: 1 = INFO, 2 = TRACE, 3 = VERBOSE",
)
@click.option(
    "otf",
    "--otf",
    is_flag=True,
    help="use to validate fuzzing outputs on the fly. If flag not set then only generation will be done",
)
@click.option("resume", "--resume", is_flag=True, help="resume from the last iteration")
@click.option(
    "evaluate",
    "--evaluate",
    is_flag=True,
    help="evaluate the generated fuzzing outputs against the oracle",
)
@click.option(
    "template",
    "--template",
    type=str,
    default=None,
    help="template to use for generation",
)
@click.option("bs", "--bs", type=int, default=1, help="batch size")
@click.option(
    "temperature", "--temperature", type=float, default=1.0, help="temperature"
)
@click.option("use_hw", "--use_hw", is_flag=True, help="use hand-written prompt")
@click.option(
    "no_input_prompt",
    "--no_input_prompt",
    is_flag=True,
    help="do not use extra input (e.g. doc or example)",
)
@click.option(
    "prompt_strategy", "--prompt_strategy", type=int, default=0, help="prompt strategy"
)
@click.option(
    "device",
    "--device",
    type=str,
    default="cuda",
    help="device to use to run the local LLM model",
)
@click.option(
    "model_name",
    "--model",
    type=str,
    default="bigcode/starcoder",
    help="model to use to run the local LLM model",
)
@click.option(
    "max_length",
    "--max_length",
    type=int,
    default=1024,
    help="max length to use to run the local LLM model",
)
def main(
    folder,
    language,
    num,
    total_time,
    level,
    otf,
    resume,
    evaluate,
    template,
    bs,
    temperature,
    use_hw,
    no_input_prompt,
    prompt_strategy,
    model_name,
    max_length,
    device,
):
    """Main function to start the fuzzing process with command line arguments."""
    target_kwargs = {
        "folder": folder,
        "language": language,
        "template": template,
        "bs": bs,
        "max_length": max_length,
        "device": device,
        "model_name": model_name,
        "temperature": temperature,
        "use_hw": use_hw,
        "no_input_prompt": no_input_prompt,
        "prompt_strategy": prompt_strategy,
        "level": level,
    }

    target = make_target(target_kwargs)
    if not evaluate:
        assert not os.path.exists(folder) or resume, f"{folder} already exists!"
        os.makedirs(folder, exist_ok=True)
        fuzz(
            target=target,
            total_time=total_time,
            number_of_iterations=num,
            output_folder=folder,
            resume=resume,
            otf=otf,
        )
    else:
        evaluate(target)


@cli.command("main_with_config")
@click.pass_context
@click.option(
    "folder",
    "--folder",
    type=str,
    default="Results/test",
    help="folder to store results",
)
def main_with_config(ctx, folder):
    """Run the main using a configuration file."""
    config_dict = ctx.obj["CONFIG_DICT"]

    print(config_dict)
    fuzzing = config_dict["fuzzing"]

    target = make_target_with_config(config_dict)
    if not fuzzing["evaluate"]:
        assert (
            not os.path.exists(folder) or fuzzing["resume"]
        ), f"{folder} already exists!"
        os.makedirs(fuzzing["output_folder"], exist_ok=True)
        fuzz(
            target=target,
            number_of_iterations=fuzzing["num"],
            total_time=fuzzing["total_time"],
            output_folder=folder,
            resume=fuzzing["resume"],
            otf=fuzzing["otf"],
        )
    else:
        evaluate(target)


if __name__ == "__main__":
    cli()
