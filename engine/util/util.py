import re


# TODO (Add other lang support): temp, only facilitate basic c/cpp syntax
def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


# most fuzzing targets should be some variation of source code
# so this function is likely fine, but we can experiment with
# other more clever variations
def simple_parse(gen_body: str):
    # first check if its a code block
    if "```" in gen_body:
        func = gen_body.split("```")[1]
        func = "\n".join(func.split("\n")[1:])
    else:
        func = ""
    return func
