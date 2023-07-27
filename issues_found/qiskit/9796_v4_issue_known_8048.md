## Environment
- **Qiskit Terra version**: 0.43.1 meta package, terra 0.24.1
- **Python version**: 3.10
- **Operating system**: docker continuumio/miniconda3

## What is happening?
Exporting a circuit with `initialize()` in QASM2 leads to invalid qasm with `reset`.

## How can we reproduce the issue?
Run this python script:

```python
from qiskit import QuantumCircuit
q = QuantumCircuit(2)
q.initialize('00')
print(q.qasm(filename="my.qasm"))
round_trip = QuantumCircuit.from_qasm_str(q.qasm())
```
Produces this output and error:
```bashcircuit-114
OPENQASM 2.0;
include "qelib1.inc";
gate state_preparation(param0,param1) q0,q1 {  }
gate initialize(param0,param1) q0,q1 { reset q0; reset q1; state_preparation(0,0) q0,q1; }
qreg q[2];
initialize(0,0) q[0],q[1];

Error near line 4 Column 27
Traceback (most recent call last):
  File "myfile.py", line 9, in <module>
    round_trip = QuantumCircuit.from_qasm_str(circuit.qasm())
  File "...qiskit/circuit/quantumcircuit.py", line 2529, in from_qasm_str
    return _circuit_from_qasm(qasm)
  File "...qiskit/circuit/quantumcircuit.py", line 4964, in _circuit_from_qasm
    ast = qasm.parse()
  File "...qiskit/qasm/qasm.py", line 53, in parse
    return qasm_p.parse(self._data)
  File "...qiskit/qasm/qasmparser.py", line 1137, in parse
    self.parser.parse(data, lexer=self.lexer, debug=self.parse_deb)
  File "...ply/yacc.py", line 333, in parse
    return self.parseopt_notrack(input, lexer, debug, tracking, tokenfunc)
  File "...ply/yacc.py", line 1120, in parseopt_notrack
    p.callable(pslice)
  File "...qiskit/qasm/qasmparser.py", line 397, in p_id_e
    raise QasmError("Expected an ID, received '" + str(program[1].value) + "'")
qiskit.qasm.exceptions.QasmError: "Expected an ID, received 'reset'"

```
The variant with `reset()` instead of `initialize()` works fine.

## What should happen?
I would expect a meaningful error when exporting if the initialize is not supported.

## Any suggestions?
The exporter should probably just fail.