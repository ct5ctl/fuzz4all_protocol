import argparse
import openai
import os
import json

from template import CPP_TEMPLATE_immediate_function, CPP_TEMPLATE_consteval, CPP_TEMPLATE_likely_unlikely
from engine.util.api_request import create_chatgpt_config, request_engine
from engine.util.util import simple_parse, comment_remover
from engine.util.Logger import Logger
from engine.generation_engine import _check_syntax_valid


def _create_chatgpt_fifo_template(system_message: str, user_message: str, prev: list):
    messages = [{"role": "system", "content": system_message}]
    for p in prev:
        if p != "":
            messages.append({"role": "user", "content": user_message})
            messages.append({"role": "assistant", "content": "```\n{}\n```".format(p)})
    messages.append({"role": "user", "content": user_message})
    return messages


def generation_fifo(args):
    logger = Logger(args.folder)
    prompt_used = CPP_TEMPLATE_likely_unlikely
    first, second, third = prompt_used['first'].strip(), prompt_used['second'].strip(), prompt_used['third'].strip()
    results = []
    for i in range(0, 5000):
        messages = _create_chatgpt_fifo_template("You are a C++ Fuzzer.", prompt_used['separator'], [first, second, third])
        config = create_chatgpt_config(prev={}, messages=messages, max_tokens=500, temperature=1)
        for message in config['messages']:
            print("{} : {}".format(message['role'], message['content']))
        ret = request_engine(config)
        func = comment_remover(simple_parse(ret["choices"][0]['message']["content"]))
        if func != "":
            logger.logo("========== sample =========")
            logger.logo(func)
            logger.logo("========== sample =========")
            with open(args.folder + "/{}.{}".format(i, args.language), "w") as f:
                f.write(func)
            results.append({"output": func, "usage": ret['usage'], "prompt": config})
            if _check_syntax_valid(func):
                if third != "":
                    first = second
                    second = third
                third = func.strip()

    with open(os.path.join(args.folder, "fuzz.json"), "w") as f:
        json.dump(results, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--key_file", type=str, default="api_key.txt")
    parser.add_argument("--language", type=str, default="c")
    args = parser.parse_args()
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    openai.api_key = open(args.key_file, 'r').read().strip()

    generation_fifo(args)


if __name__ == "__main__":
    main()
