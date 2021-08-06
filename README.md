# Transition_Reduced_Circular_Shift

## Table of contents
* [Description](#description)
* [Circuit Patterns](#circuit-patterns)
* [Code Implementation](#code-implementation)
* [Acknowledgements](#acknowledgements)
* [Notes](#notes)

# Description
Circuit identity for faster reversible nearest-neighbour circular shift with CNOT gates.

# Circuit Patterns
![Circuit patterns image](./patterns.png)

# Code Implementation
The tReduced.py program includes a function t_reduced which will add the
T-Reduced pattern to a qiskit QuantumCircuit along a given path of
QuantumRegister's.
Here is an example implementation of the t_reduced function:
```
from qiskit import QuantumCircuit, QuantumRegister
from tReduced import t_reduced

qubits = 8
qr = QuantumRegister(qubits, name = "q")
qc = QuantumCircuit(qr)

t_reduced(qc, [0, 1, 2, 3, 4, 5, 6, 7])
```

# Acknowledgements
This work was completed as part of my undergrad thesis. I would like to thank my
professors Rajesh Pereira and Joe Sawada for co-supervising my thesis and
contributing to this work.

# Notes
I don't know if the C-Reduced, S-Reduced, or T-Reduced patterns are novel. If
anyone knows of previous publications of these patterns please create an issue
so that they can be properly credited.
