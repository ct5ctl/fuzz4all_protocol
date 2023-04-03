EXAMPLE_SMT_TEMPLATE = {
    "separator": 'Please create a fuzzing testcase for a SMT solver',
    "first":
        """
(set-logic QF_LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (- x y) (+ x (- y) 1)))
(check-sat)
(exit)
""",
    "second":
        """
(set-logic QF_UF)
(declare-const p Bool)
(assert (and p (not p))) 
(check-sat)
(exit)
""",
    "third":
        """
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
"""
}