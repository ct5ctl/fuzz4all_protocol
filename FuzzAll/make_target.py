from FuzzAll.target.CPP.CPP import CPPTarget
from FuzzAll.target.GO.GO import GOTarget
from FuzzAll.target.JAVA.JAVA import JAVATarget
from FuzzAll.target.SMT.SMT import SMTTarget


def make_target(args, parser):
    parser.add_argument(
        "--template",
        type=str,
        required=True,
        help="""
        template file to use for the target.
        Go to the main py file of the target (e.g. FuzzAll/target/CPP/CPP.py)
        to see the template files which are supported for each target.
    """,
    )
    parser.add_argument("--bs", type=int, required=True, help="batch size")
    parser.add_argument(
        "--temperature",
        type=float,
        required=True,
        help="temperature to query the LLM model when generating output.",
    )
    parser.add_argument("--use_hw", action="store_true")
    parser.add_argument(
        "--prompt_strategy",
        type=int,
        required=True,
        help="""
            prompt strategy to generate obtain programs after the first one.
                0: generate new code using separator
                1: mutate existing code
                2: semantically equivalent code generation
                3: combine previous two code generations
            """,
    )
    args = parser.parse_args()
    if args.language == "cpp":  # GCC
        return args, CPPTarget(
            language="cpp",
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            use_kw=args.use_hw,
            prompt_strategy=args.prompt_strategy,
            level=args.level,
        )
    elif args.language == "smt2":  # SMT solvers
        return args, SMTTarget(
            language=args.language,
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            use_kw=args.use_hw,
            prompt_strategy=args.prompt_strategy,
            level=args.level,
        )
    elif args.language == "go":  # GO
        return args, GOTarget(
            language=args.language,
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            use_kw=args.use_hw,
            prompt_strategy=args.prompt_strategy,
            level=args.level,
        )
    elif args.language == "java":  # Java
        return args, JAVATarget(
            language=args.language,
            folder=args.folder,
            template=args.template,
            bs=args.bs,
            temperature=args.temperature,
            use_kw=args.use_hw,
            prompt_strategy=args.prompt_strategy,
            level=args.level,
        )
    else:
        raise ValueError(f"Invalid target {args.language}")
