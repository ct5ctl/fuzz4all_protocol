from FuzzAll.target.CPP.GPP12 import GPP12Target
from FuzzAll.target.GO.GO import GOTarget
from FuzzAll.target.SMT.SMT import SMTTarget


def make_target(args, parser):
    if args.language == "cpp":  # GCC
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
            level=args.level,
        )
    elif args.language == "smt2":  # SMT solvers
        parser.add_argument("--template", type=str, required=True)
        parser.add_argument("--bs", type=int, required=True)
        parser.add_argument("--temperature", type=float, required=True)
        args = parser.parse_args()
        return args, SMTTarget(
            language=args.language,
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            level=args.level,
        )
    elif args.language == "go":  # GO
        parser.add_argument("--template", type=str, required=True)
        parser.add_argument("--bs", type=int, required=True)
        parser.add_argument("--temperature", type=float, required=True)
        args = parser.parse_args()
        return args, GOTarget(
            language=args.language,
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            level=args.level,
        )
    else:
        raise ValueError(f"Invalid target {args.language}")
