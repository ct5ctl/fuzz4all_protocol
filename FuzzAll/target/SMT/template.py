EXAMPLE_SMT_TEMPLATE = {
    "separator": "Please create a fuzzing testcase for a SMT solver",
    "first": """
(set-logic QF_LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
(exit)
""",
    "second": """
(set-logic QF_UF)
(declare-const p Bool)
(assert (and p (not p)))
(check-sat)
(exit)
""",
    "third": """
(set-logic QF_BV)
(declare-const x_0 (_ BitVec 32))
(declare-const x_1 (_ BitVec 32))
(declare-const x_2 (_ BitVec 32))
(declare-const y_0 (_ BitVec 32))
(declare-const y_1 (_ BitVec 32))
(assert (= x_1 (bvadd x_0 y_0)))
(assert (= y_1 (bvsub x_1 y_0)))
(assert (= x_2 (bvsub x_1 y_1)))
(assert (not
  (and (= x_2 y_0)
       (= y_1 x_0))))
(check-sat)
(exit)
""",
}


CRASH_SMT_TEMPLATE = {
    "separator": "Please create a complex SMT formula as input to an SMT solver",
    "first": """
(define-fun a () Float16 (fp #b1 #b00000 #b0000000011))
(define-fun l () Float16 (fp #b1 #b00000 #b0000000001))
(declare-fun b () Float16)
(declare-fun r () Float16)
(assert (= l (fp.abs b) r (fp.rem a b)))
(check-sat)
(exit)
""",
    "second": """
(declare-sort U 0)
(declare-fun R (U U) Bool)
(assert (forall ((x U) (y U)) (= (R x y) ((_ transitive-closure 0) x y))))
(declare-fun a () U)
(assert (not (R a a)))
(check-sat)
(exit)
""",
    "third": """
(declare-fun fp () (_ FloatingPoint 3 2))
(assert (= (fp (_ bv0 1) (_ bv0 3) (_ bv0 1)) (fp.fma roundNearestTiesToEven fp fp (fp (_ bv0 1) (_ bv0 3) (_ bv0 1)))))
(check-sat)
(exit)
""",
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
