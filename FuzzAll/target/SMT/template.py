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
