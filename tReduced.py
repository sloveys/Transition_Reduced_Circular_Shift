"""
Samuel Crawford Loveys
© 2021

Function for constructing nearest-neighbour circular shift with CNOT gates.

Calls qiskit methods for applying CNOT (cx) gates.

'up' is a keyword indecator for specifying the alternative versions of the
patterns provided here.
"""


def _cxWalk(qc, path, up = False):
    """
    Creates a series of CNOT gates along the path of qubits.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (int array) to apply to qc
    up: Default = False
        True implements "cx qr1, qr0; cx qr2, qr1; ...", where qr is a quantum register in the path
        False implements "cx qr0, qr1; cx qr1, qr2; ...", where qr is a quantum register in the path
    """

    # up index (1 inverts direction)
    upi = 0
    if (up):
        upi = 1

    for i in range(len(path) - 1):
        qc.cx(path[i + upi], path[i + 1 - upi])

def tReduced(qc, path, up = False, transitionQubit = None):
    """
    Adds T-Reduced shift pattern to circuit along path. Completes circular shift
    with a depth of n + 6 and 4n - 2 CNOT gates for default values of
    transitionQubit and n > 2, where n is the number of connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (int array) to apply to qc
    up: Default = False
        True implements UDT-Reduced
        False implements DUT-Reduced
    transitionQubit: integer index of the transition qubit between C-Reduced and S-Reduced patterns
        Defualt = floor(n / 2), where n is the number of connections in the path
        Acceptable values of k are in the range [0, len(path) - 1]
    """

    if (transitionQubit == None):
        transitionQubit = (len(path) - 1) // 2
    else:
        assert transitionQubit >= 0 and transitionQubit < len(path)

    crpath = path[:transitionQubit + 1] # C-Reduced path
    cpath = list(reversed(path[:transitionQubit])) # cleanup step path

    srpath = path[transitionQubit:] # S-Reduced path
    spath = list(reversed(path[transitionQubit + 1:])) # setup step path

    # setup step
    _cxWalk(qc, spath, up = up)

    # begin C-Reduced transfer step
    _cxWalk(qc, crpath, up = up)

    # integrated transfer step
    _cxWalk(qc, path, up = not up)
    _cxWalk(qc, path, up = up)

    # end S-Reduced transfer step
    _cxWalk(qc, srpath, up = not up)

    # cleanup step
    _cxwalk(qc, cpath, up = not up)
