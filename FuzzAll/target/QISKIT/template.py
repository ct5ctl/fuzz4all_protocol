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
