qiskit_parameter = {
    "docstring": """
Qiskit documentation > Qiskit Terra API Reference > Quantum Circuits (qiskit.circuit) > Parameter
Parameter¶
CLASSParameter(name, uuid=None)[SOURCE]¶
Bases: ParameterExpression

Parameter Class for variable parameters.

A parameter is a variable value that is not required to be fixed at circuit definition.
""",
    "hw_prompt": """
`qiskit.circuit > Parameters`
Description:
```
CLASSParameter(name, uuid=None)[SOURCE]¶
Bases: ParameterExpression

Parameter Class for variable parameters.

A parameter is a variable value that is not required to be fixed at circuit definition.
```
""",
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    # "separator": 'Please create a short but complex program which combines many new features of C++ with std::optional',
    "separator": "''' Please create a very short program which combines QuantumCircuit and parameters in a complex way. Create a quantum circuit object qc as global variable with this quantum circuit. '''",
    "begin": "from qiskit import QuantumCircuit",
    "target_api": "Parameter",
    # "separator": 'Please create a short program which has complex usages of std::optional',
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    "example_code": """
Here is an example program using Parameter
```
>>> from qiskit.circuit import QuantumCircuit, Parameter
>>> a, b, elephant = Parameter("a"), Parameter("b"), Parameter("elephant")
>>> circuit = QuantumCircuit(1)
>>> circuit.rx(b, 0)
>>> circuit.rz(elephant, 0)
>>> circuit.ry(a, 0)
>>> circuit.parameters  # sorted alphabetically!
ParameterView([Parameter(a), Parameter(b), Parameter(elephant)])
```
""",
}

qiskit_basic = {
    "docstring": """
    Here, we provide an overview of working with Qiskit. The fundamental package of Qiskit is Terra that provides the basic building blocks necessary to program quantum computers. The fundamental unit of Qiskit is the quantum circuit. A basic workflow using Qiskit consists of two stages: Build and Execute. Build allows you to make different quantum circuits that represent the problem you are solving, and Execute that allows you to run them on different backends. After the jobs have been run, the data is collected and postprocessed depending on the desired output.

import numpy as np
from qiskit import *

Circuit Basics¶
Building the circuit¶
The basic element needed for your first program is the QuantumCircuit. We begin by creating a QuantumCircuit comprised of three qubits.

# Create a Quantum Circuit acting on a quantum register of three qubits
circ = QuantumCircuit(3)
After you create the circuit with its registers, you can add gates (“operations”) to manipulate the registers. As you proceed through the tutorials you will find more gates and circuits; below is an example of a quantum circuit that makes a three-qubit GHZ state

To create such a state, we start with a three-qubit quantum register. By default, each qubit in the register is initialized to
. To make the GHZ state, we apply the following gates: - A Hadamard gate
 on qubit
, which puts it into the superposition state
. - A controlled-Not operation (
) between qubit
 and qubit
. - A controlled-Not operation between qubit
 and qubit
.

On an ideal quantum computer, the state produced by running this circuit would be the GHZ state above.

In Qiskit, operations can be added to the circuit one by one, as shown below.

# Add a H gate on qubit $q_{0}$, putting this qubit in superposition.
circ.h(0)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{1}$, putting
# the qubits in a Bell state.
circ.cx(0, 1)
# Add a CX (CNOT) gate on control qubit $q_{0}$ and target qubit $q_{2}$, putting
# the qubits in a GHZ state.
circ.cx(0, 2)
""",
    "hw_prompt": """
QuantumCircuit object: Create a new circuit. A circuit is a list of instructions bound to some registers.
transpile: Transpile one or more circuits, according to some desired transpilation targets.
""",
    "separator": "'''Create a complex and advanced QuantumCircuit and transpile.'''",
    "begin": "from qiskit import QuantumCircuit\nfrom qiskit.compiler import transpile",
    "target_api": "transpile(",
    "example_code": """
from time import time
from qiskit.transpiler import CouplingMap
from qiskit.providers.models import BackendProperties
from qiskit.circuit import qpy_serialization
with open('circuit.qpy', 'rb') as fd:
    new_qc = qpy_serialization.load(fd)[0]

coupling_map=backend.configuration().coupling_map
backend_properties=backend.properties()
basis_gates=backend.configuration().basis_gates

transpile(new_qc,
          backend_properties=backend_properties,
          coupling_map=CouplingMap(coupling_map),
          optimization_level=3,
          basis_gates=basis_gates,
          seed_transpiler=0
          )
          """,
}


qiskit_hw_transpile = {
    "docstring": "",
    "example_code": "",
    "hw_prompt": """
QuantumCircuit object: Create a new circuit. A circuit is a list of instructions bound to some registers.
transpile function: Transpile the circuit transpile(qc, etc), where qc is the circuit to transpile.
""",
    "separator": "'''Create a QuantumCircuit and transpile.'''",
    "begin": "from qiskit import QuantumCircuit\nfrom qiskit.compiler import transpile\n\n",
    "target_api": "transpile(",
}

qiskit_hw_qasm = {
    "docstring": "",
    "example_code": "",
    "hw_prompt": """
QuantumCircuit object: Create a new circuit. A circuit is a list of instructions bound to some registers.
export to QASM function: Save the circuit as qasm file via the call qc.qasm(filename='output.qasm'), where qc is the circuit to transpile.
""",
    "separator": "'''Create a QuantumCircuit and save it as qasm.'''",
    "begin": "from qiskit import QuantumCircuit\n\n",
    "target_api": "qasm(",
}
