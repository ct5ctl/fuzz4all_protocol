# https://qiskit.org/documentation/tutorials/circuits/1_getting_started_with_qiskit.html
# Accessed 2023-07-12

Getting Started with Qiskit¶
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
<qiskit.circuit.instructionset.InstructionSet at 0x7fcdc4469c10>
Visualize Circuit¶
You can visualize your circuit using Qiskit QuantumCircuit.draw(), which plots the circuit in the form found in many textbooks.

OpenQASM backend¶
The simulators above are useful because they provide information about the state output by the ideal circuit and the matrix representation of the circuit. However, a real experiment terminates by measuring each qubit (usually in the computational
 basis). Without measurement, we cannot gain information about the state. Measurements cause the quantum system to collapse into classical bits.

For example, suppose we make independent measurements on each qubit of the three-qubit GHZ state

and let
 denote the bitstring that results. Recall that, under the qubit labeling used by Qiskit,
 would correspond to the outcome on qubit
,
 to the outcome on qubit
, and
 to the outcome on qubit
.

Note: This representation of the bitstring puts the most significant bit (MSB) on the left, and the least significant bit (LSB) on the right. This is the standard ordering of binary bitstrings. We order the qubits in the same way (qubit representing the MSB has index 0), which is why Qiskit uses a non-standard tensor product order.

Recall the probability of obtaining outcome
 is given by

and as such for the GHZ state probability of obtaining 000 or 111 are both 1/2.

To simulate a circuit that includes measurement, we need to add measurements to the original circuit above, and use a different Aer backend.

# Create a Quantum Circuit
meas = QuantumCircuit(3, 3)
meas.barrier(range(3))
# map the quantum measurement to the classical bits
meas.measure(range(3), range(3))

# The Qiskit circuit object supports composition using
# the compose method.
circ.add_register(meas.cregs[0])
qc = circ.compose(meas)

#drawing the circuit
qc.draw()
     ┌───┐           ░ ┌─┐
q_0: ┤ H ├──■────■───░─┤M├──────
     └───┘┌─┴─┐  │   ░ └╥┘┌─┐
q_1: ─────┤ X ├──┼───░──╫─┤M├───
          └───┘┌─┴─┐ ░  ║ └╥┘┌─┐
q_2: ──────────┤ X ├─░──╫──╫─┤M├
               └───┘ ░  ║  ║ └╥┘
c: 3/═══════════════════╩══╩══╩═
                        0  1  2
This circuit adds a classical register, and three measurements that are used to map the outcome of qubits to the classical bits.

To simulate this circuit, we use the qasm_simulator in Qiskit Aer. Each run of this circuit will yield either the bitstring 000 or 111. To build up statistics about the distribution of the bitstrings (to, e.g., estimate
), we need to repeat the circuit many times. The number of times the circuit is repeated can be specified in the run method, via the shots keyword.

# Use Aer's qasm_simulator
backend_sim = Aer.get_backend('qasm_simulator')

# Execute the circuit on the qasm simulator.
# We've set the number of repeats of the circuit
# to be 1024, which is the default.
job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)

# Grab the results from the job.
result_sim = job_sim.result()
Once you have a result object, you can access the counts via the function get_counts(circuit). This gives you the aggregated binary outcomes of the circuit you submitted.

counts = result_sim.get_counts(qc)
print(counts)
{'111': 487, '000': 537}
Approximately 50 percent of the time, the output bitstring is 000. Qiskit also provides a function plot_histogram, which allows you to view the outcomes.

QuantumCircuit object: Create a new circuit. A circuit is a list of instructions bound to some registers.
transpile function: Transpile the circuit transpile(qc, etc), where qc is the circuit to transpile.
