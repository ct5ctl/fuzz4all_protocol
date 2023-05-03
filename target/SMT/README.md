# SMT Solver

## Setup

### Z3

clone the most recent version of Z3

```shell
cd z3
python scripts/mk_make.py --debug  # compile with debug flag
cd build/
make
sudo make install # install to path
```

### CVC5

clone the most recent version of cvc5

```shell
cd cvc5
./configure.sh production --assertions --auto-download # use --assertion to enable debug assertions
cd build/
make
sudo make install # install to path
```

## Oracle

The oracle is through differential testing. We follow the classic work of "On the Unusual Effectiveness of Type-Aware Operator
Mutations for Testing SMT Solvers"

Our differential testing setup is through Z3 and CvC5
- crash bugs: Formula 𝜑 triggers a soundness bug if solvers 𝑆1 and 𝑆2 both do not crash
and give different satisfiabilities for 𝜑.
- invalid model bugs: Formula 𝜑 triggers an invalid model bug if the model returned by the
solver does not satisfy 𝜑.
- soundness bugs: Formula 𝜑 triggers a crash bug if the solver throws out an assertion violation or a
segmentation fault while solving 𝜑.

## Things to Note
