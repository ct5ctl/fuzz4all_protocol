## Environment
- **Qiskit Terra version**: 0.43.1 meta package, terra 0.24.1
- **Python version**: 3.10
- **Operating system**: docker continuumio/miniconda3

## What is happening?
Exporting a circuit with a sub-circuit via `append()` and that uses `measure()` leads to an invalid qasm file, generating error when imported again.

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
```bash
Converting to qasm and back for circuit circuit-114
     ┌───┐     ┌─┐   ┌──────────────┐
q_0: ┤ H ├──■──┤M├───┤0             ├
     └───┘┌─┴─┐└╥┘┌─┐│              │
q_1: ─────┤ X ├─╫─┤M├┤1             ├
          └───┘ ║ └╥┘│  circuit-115 │
c_0: ═══════════╩══╬═╡0             ╞
                   ║ │              │
c_1: ══════════════╩═╡1             ╞
                     └──────────────┘
OPENQASM 2.0;
include "qelib1.inc";
gate circuit_115 q0,q1 { h q0; cx q0,q1; measure q0; measure q1; }
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
circuit_115 q[0],q[1],c[0],c[1];

Error near line 3 Column 15
Traceback (most recent call last):
  File "myfile.py", line 16, in <module>
    QuantumCircuit().from_qasm_str(circuit2.qasm())
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
qiskit.qasm.exceptions.QasmError: "Expected an ID, received 'measure'"

```
The qasm contains also a second error leading to an error, thus the fact that `circuit_115` is defined with 2 qubits, but then it is used with 4 arguments (see: https://github.com/Qiskit/qiskit-terra/issues/7750#issue-1163308223)

## What should happen?
I would expect a valid qasm since the circuit is theoretically representable in qasm.

## Any suggestions?
What about expanding the definition and injecting the basic instructions directly in the main code, without a separate definition, thus avoiding the problem with the `measure` and number of arguments?
This would clearly lead to a bigger qasm file, but it would be valid.