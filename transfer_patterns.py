"""
Samuel Crawford Loveys
© 2021

Functions for constructing nearest-neighbour circular shift and transfer with CNOT gates.

Calls qiskit methods for applying CNOT (cx) gates.

'up' is a keyword indecator for specifying the alternative versions of the
patterns provided here.
"""

def _cx_walk(qc, path, up = False):
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

def z_transfer(qc, path, up = False):
    """
    Implements Z-Transfer transfer pattern to circuit along a path. Completes
    transfer across zeroed states with a depth of n + 2 and 2n CNOT gates, where
    n is the number of connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
    up: Default = False
        True raises AssertionError
        False implements Z-Transfer
    """
    assert not up # Z-Transfer-Up is an invalid pattern

    _cx_walk(qc, path)
    _cx_walk(qc, path, up = True)

def g_transfer(qc, path, up = False):
    """
    Implements G-Transfer transfer pattern to circuit along a path. Completes
    transfer across zeroed xor garbage states with a depth of n + 4 and 3n CNOT
    gates, where n is the number of connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
    up: Default = False
        True implements G-Transfer-Up
        False implements G-Transfer-Down
    """
    _cx_walk(qc, path, up = up)
    _cx_walk(qc, path, up = not up)
    _cx_walk(qc, path, up = up)

def s_shift(qc, path, up = False):
    """
    Implements S-Shift shift pattern to circuit along a path. Completes circular
    shift with a depth of 3n and 3n CNOT gates, where n is the number of
    connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
    up: Default = False
        True implements S-Shift-Up
        False implements S-Shift-Down
    """
    def _swap(qc, qr0, qr1):
        """
        Implements SWAP-Up relative to the path [qr0, qr1].
        qc: the QuantumCircuit object
        qr0: first QuantumRegister object or quantum register index (int) in the path
        qr1: second QuantumRegister object or quantum register index (int) in the path
        """
        qc.cx(qr0, qr1)
        qc.cx(qr1, qr0)
        qc.cx(qr0, qr1)

    # up index (1 inverts direction)
    upi = 0
    if (up):
        upi = 1

    for i in range(len(path) - 1):
        _swap(qc, path[i + upi], path[i + 1 - upi])

def c_reduced(qc, path, up = False):
    """
    Wrapper function using t_reduced.
    Implements C-Reduced shift pattern to circuit along a path. Completes
    circular shift with a depth of 2n + 3 and 4n - 1 CNOT gates when n > 1,
    where n is the number of connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
    up: Default = False
        True implements C-Reduced-Up
        False implements C-Reduced-Down
    """
    t_reduced(qc, path, up = up, transitionQubit = len(path) - 1)

def s_reduced(qc, path, up = False):
    """
    Wrapper function using t_reduced.
    Implements S-Reduced shift pattern to circuit along a path. Completes
    circular shift with a depth of 2n + 3 and 4n - 1 CNOT gates when n > 1,
    where n is the number of connections in the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
    up: Default = False
        True implements S-Reduced-Up
        False implements S-Reduced-Down
    """
    t_reduced(qc, path, up = not up, transitionQubit = 0)

def t_reduced(qc, path, up = False, transitionQubit = None):
    """
    Implements T-Reduced shift pattern to circuit along a path. Completes
    circular shift with a depth of n + 6 and 4n - 2 CNOT gates for default
    values of transitionQubit and n > 2, where n is the number of connections in
    the path.
    qc: the QuantumCircuit object
    path: list of QuantumRegister objects or quantum register indices (list<int>) to apply to qc
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
    _cx_walk(qc, spath, up = up)

    # begin C-Reduced transfer step
    _cx_walk(qc, crpath, up = up)

    # integrated transfer step
    _cx_walk(qc, path, up = not up)
    _cx_walk(qc, path, up = up)

    # end S-Reduced transfer step
    _cx_walk(qc, srpath, up = not up)

    # cleanup step
    _cx_walk(qc, cpath, up = not up)
