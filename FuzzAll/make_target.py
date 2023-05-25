from FuzzAll.target.CPP.GPP12 import GPP12Target
from FuzzAll.target.SMT.SMT import SMTTarget
from FuzzAll.target.target import Target


def make_target(args, parser):
    if args.language == "cpp":
        parser.add_argument("--template", type=str, required=True)
        parser.add_argument("--bs", type=int, required=True)
        parser.add_argument("--temperature", type=float, required=True)
        args = parser.parse_args()
        return args, GPP12Target(
            language="cpp",
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
        )
    elif args.language == "smt2":  # SMT solvers
        parser.add_argument("--template", type=str, required=True)
        args = parser.parse_args()
        return args, SMTTarget(language=args.language, folder=args.folder)
    else:
        raise ValueError(f"Invalid target {args.language}")
