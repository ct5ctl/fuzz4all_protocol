smt2_general = {
    "hw_prompt": """
SMT2 is a standardized input language supported by many SMT solvers. Its syntax is based on S-expressions, inspired by languages in the LISP family. We review some basic elements of its syntax here, particularly the parts that are used by F*’s SMT encoding.
Multi-sorted logic
The logic provided by the SMT solver is multi-sorted: the sorts provide a simple type system for the logic, ensuring, e.g., that terms from two different sorts can never be equal. A user can define a new sort T, as shown below:
(declare-sort T)
Every sort comes with a built-in notion of equality. Given two terms p and q of the same sort T, (= p q) is a term of sort Bool expressing their equality.
Declaring uninterpreted functions
A new function symbol F, with arguments in sorts sort_1 .. sort_n and returning a result in sort is declared as shown below,
(declare-fun F (sort_1 ... sort_n) sort)
The function symbol F is uninterpreted, meaning that the only information the solver has about F is that it is a function, i.e., when applied to equal arguments F produces equal results.
SMT2 provides support for several theories, notably integer and real arithmetic. For example, on terms i and j of Int sort, the sort of unbounded integers, the following terms define the expected arithmetic functions:
SMT2 provides basic logical connectives as shown below, where p and q are terms of sort Bool
)
""",
    "docstring": """
SMT2 is a standardized input language supported by many SMT solvers. Its syntax is based on S-expressions, inspired by languages in the LISP family. We review some basic elements of its syntax here, particularly the parts that are used by F*’s SMT encoding.

Multi-sorted logic

The logic provided by the SMT solver is multi-sorted: the sorts provide a simple type system for the logic, ensuring, e.g., that terms from two different sorts can never be equal. A user can define a new sort T, as shown below:

(declare-sort T)
Every sort comes with a built-in notion of equality. Given two terms p and q of the same sort T, (= p q) is a term of sort Bool expressing their equality.

Declaring uninterpreted functions

A new function symbol F, with arguments in sorts sort_1 .. sort_n and returning a result in sort is declared as shown below,

(declare-fun F (sort_1 ... sort_n) sort)
The function symbol F is uninterpreted, meaning that the only information the solver has about F is that it is a function, i.e., when applied to equal arguments F produces equal results.

Theory symbols

SMT2 provides support for several theories, notably integer and real arithmetic. For example, on terms i and j of Int sort, the sort of unbounded integers, the following terms define the expected arithmetic functions:

(+ i j)       ; addition
(- i j)       ; subtraction
(* i j)       ; multiplication
(div i j)     ; Euclidean division
(mod i j)     ; Euclidean modulus
Logical connectives

SMT2 provides basic logical connectives as shown below, where p and q are terms of sort Bool

(and p q)                ; conjunction
(or p q)                 ; disjunction
(not p)                  ; negation
(implies p q)            ; implication
(iff p q)                ; bi-implication
SMT2 also provides support for quantifiers, where the terms below represent a term p with the variables x1 ... xn universally and existentially quantified, respectively.

(forall ((x1 sort_1) ... (xn sort_n)) p)
(exists ((x1 sort_1) ... (xn sort_n)) p)
Attribute annotations

A term p can be decorated with attributes names a_1 .. a_n with values v_1 .. v_n using the following syntax—the ! is NOT to be confused with logical negation.

(! p
   :a_1 v_1
   ...
   :a_n v_n)
A common usage is with quantifiers, as we’ll see below, e.g.,

(forall ((x Int))
        (! (implies (>= x 0) (f x))
           :qid some_identifier))
An SMT2 theory and check-sat

An SMT2 theory is a collection of sort and function symbol declarations, and assertions of facts about them. For example, here’s a simple theory declaring a function symbol f and an assumption that f x y is equivalent to (>= x y)—note, unlike in F*, the assert keyword in SMT2 assumes that a fact is true, rather than checking that it is valid, i.e., assert in SMT2 is like assume in F*.

(declare-fun f (Int Int) Bool)

(assert (forall ((x Int) (y Int))
                (iff (>= y x) (f x y))))
In the context of this theory, one can ask whether some facts about f are valid. For example, to check if f is a transitive function, one asserts the negation of the transitivity property for f and then asks solver to check (using the (check-sat) directive) if the resulting theory is satisfiable.

(assert (not (forall ((x Int) (y Int) (z Int))
                     (implies (and (f x y) (f y z))
                              (f x z)))))
(check-sat)
In this case, the solver very quickly responds with unsat, meaning that there are no models for the theory that contain an interpretation of f compatible with both assertions, or, equivalently, the transitivity of f is true in all models. That is, we expect successful queries to return unsat.
    """,
    "separator": "; Please create a short program which uses complex SMT2 logic for an SMT solver",
    "begin": "(set-logic ALL)",
}

smt2_lia = {
    "hw_prompt": """
    (logic LIA
 :theories (Ints)
 :language
 "Closed formulas built over an arbitrary expansion of the
  Ints signature with free constant symbols, but whose terms of sort Int
  are all linear, that is, have no occurrences of the function symbols
  *, /, div, mod, and abs, except as specified the :extensions attribute.
 "
 :extensions
 "Terms with _concrete_ coefficients are also allowed, that is, terms
  of the form c, (* c x), or (* x c)  where x is a free constant and
  c is a term of the form n or (- n) for some numeral n.
 "
)
    """,
    "docstring": """
    (logic LIA

 :smt-lib-version 2.6
 :smt-lib-release "2017-11-24"
 :written-by "Cesare Tinelli"
 :date "2016-02-07"
 :update-history
 "Note: history only accounts for content changes, not release changes.
 "
 :theories (Ints)

 :language
 "Closed formulas built over an arbitrary expansion of the
  Ints signature with free constant symbols, but whose terms of sort Int
  are all linear, that is, have no occurrences of the function symbols
  *, /, div, mod, and abs, except as specified the :extensions attribute.
 "

 :extensions
 "Terms with _concrete_ coefficients are also allowed, that is, terms
  of the form c, (* c x), or (* x c)  where x is a free constant and
  c is a term of the form n or (- n) for some numeral n.
 "
)
    """,
    "separator": "; Please create a short program which uses complex LIA logic for an SMT solver",
    "begin": "(set-logic LIA)",
}

smt2_lia_example = {
    "hw_prompt": """
(set-logic LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
; unsat
(exit)""",
    "docstring": """
(set-logic LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
; unsat
(exit)""",
    "separator": "; Please create a short program which uses complex LIA logic for an SMT solver",
    "begin": "(set-logic LIA)",
}

smt2_lia_example_doc = {
    "hw_prompt": """
(logic AUFLIA
 :theories (Ints ArraysEx)

 :language
 "Closed formulas built over arbitrary expansions of the Ints and ArraysEx
  signatures with free sort and function symbols, but with the following
  restrictions:
  - all terms of sort Int are linear, that is, have no occurrences of the
    function symbols *, /, div, mod, and abs, except as specified in the
    :extensions attributes;
  - all array terms have sort (Array Int Int).
 "

 :extensions
 "As in the logic QF_AUFLIA."

:notes
 "This logic properly extends the logic QF_AUFLIA by allowing quantifiers."
)

(set-logic LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
; unsat
(exit)""",
    "docstring": """
(logic AUFLIA
 :theories (Ints ArraysEx)

 :language
 "Closed formulas built over arbitrary expansions of the Ints and ArraysEx
  signatures with free sort and function symbols, but with the following
  restrictions:
  - all terms of sort Int are linear, that is, have no occurrences of the
    function symbols *, /, div, mod, and abs, except as specified in the
    :extensions attributes;
  - all array terms have sort (Array Int Int).
 "

 :extensions
 "As in the logic QF_AUFLIA."

:notes
 "This logic properly extends the logic QF_AUFLIA by allowing quantifiers."
)

(set-logic LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
; unsat
(exit)""",
    "separator": "; Please create a short program which uses complex LIA logic for an SMT solver",
    "begin": "(set-logic LIA)",
}

smt2_auflia = {
    "hw_prompt": """
(logic AUFLIA
 :theories (Ints ArraysEx)

 :language
 "Closed formulas built over arbitrary expansions of the Ints and ArraysEx
  signatures with free sort and function symbols, but with the following
  restrictions:
  - all terms of sort Int are linear, that is, have no occurrences of the
    function symbols *, /, div, mod, and abs, except as specified in the
    :extensions attributes;
  - all array terms have sort (Array Int Int).
 "

 :extensions
 "As in the logic QF_AUFLIA."

:notes
 "This logic properly extends the logic QF_AUFLIA by allowing quantifiers."
)
    """,
    "docstring": """
(logic AUFLIA

 :smt-lib-version 2.6
 :smt-lib-release "2017-11-24"
 :written-by "Cesare Tinelli"
 :date "2010-04-30"
 :last-updated "2015-04-25"
 :update-history
 "Note: history only accounts for content changes, not release changes.
  2015-04-25 Updated to Version 2.5.
 "

 :theories (Ints ArraysEx)

 :language
 "Closed formulas built over arbitrary expansions of the Ints and ArraysEx
  signatures with free sort and function symbols, but with the following
  restrictions:
  - all terms of sort Int are linear, that is, have no occurrences of the
    function symbols *, /, div, mod, and abs, except as specified in the
    :extensions attributes;
  - all array terms have sort (Array Int Int).
 "

 :extensions
 "As in the logic QF_AUFLIA."

:notes
 "This logic properly extends the logic QF_AUFLIA by allowing quantifiers."
)
    """,
    "separator": "; Please create a short program which uses complex AUFLIA logic for an SMT solver",
    "begin": "(set-logic AUFLIA)",
}

smt2_lra = {
    "hw_prompt": """
(logic LRA
 :theories (Reals)

 :language
 "Closed formulas built over arbitrary expansions of the Reals signature
  with free constant symbols, but containing only linear atoms, that is,
  atoms with no occurrences of the function symbols * and /, except as
  specified the :extensions attribute.
 "

 :extensions
 "Terms with _concrete_ coefficients are also allowed, that is, terms
  of the form c, (* c x), or (* x c)  where x is a free constant and
  c is an integer or rational coefficient.
  - An integer coefficient is a term of the form m or (- m) for some
    numeral m.
  - A rational coefficient is a term of the form d, (- d) or (/ c n)
    for some decimal d, integer coefficient c and numeral n other than 0.
 "

:notes
 "This logic properly extends the logic QF_LRA by allowing quantifiers."
)
    """,
    "docstring": """
(logic LRA

 :smt-lib-version 2.6
 :smt-lib-release "2017-11-24"
 :written-by "Cesare Tinelli"
 :date "2010-05-11"
 :last-updated "2015-04-25"
 :update-history
 "Note: history only accounts for content changes, not release changes.
  2015-04-25 Updated to Version 2.5.
  2011-06-03 Replaced ''(* c x), or (* x c)'' with ''c, (* c x), or (* x c)''
             in :extensions.
             (The missing case was had been left out unintentionally.)
 "

 :theories (Reals)

 :language
 "Closed formulas built over arbitrary expansions of the Reals signature
  with free constant symbols, but containing only linear atoms, that is,
  atoms with no occurrences of the function symbols * and /, except as
  specified the :extensions attribute.
 "

 :extensions
 "Terms with _concrete_ coefficients are also allowed, that is, terms
  of the form c, (* c x), or (* x c)  where x is a free constant and
  c is an integer or rational coefficient.
  - An integer coefficient is a term of the form m or (- m) for some
    numeral m.
  - A rational coefficient is a term of the form d, (- d) or (/ c n)
    for some decimal d, integer coefficient c and numeral n other than 0.
 "

:notes
 "This logic properly extends the logic QF_LRA by allowing quantifiers."
)
    """,
    "separator": "; Please create a short program which uses complex LRA logic for an SMT solver",
    "begin": "(set-logic LRA)",
}
