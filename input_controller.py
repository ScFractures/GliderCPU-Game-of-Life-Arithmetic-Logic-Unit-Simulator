import golly as g

# ============================================================
# EATER DEFINITIONS
# ============================================================

def left_eater(x, y):
    return [
        (x, y),
        (x + 1, y),

        (x, y + 1),

        (x + 1, y + 2),
        (x + 2, y + 2),
        (x + 3, y + 2),

        (x + 3, y + 3)
    ]

# ============================================================
# GATE DATABASE
# ============================================================

GATES = {

    "AND": {
        "file": "and_gate.rle",

        "A": left_eater(-41, -20),
        "B": left_eater(5, -21),

        "OUT": (17, 35)
    },

    "OR": {
        "file": "or_gate.rle",

        "A": left_eater(-19, -34),
        "B": left_eater(27, -35),

        "OUT": (18, 41)
    },

    "NOT": {
        "file": "not_gate.rle",

        "A": left_eater(-21, -4),

        "OUT": (-20, 25)
    },

    "XOR": {
        "file": "xor_gate.rle",

        "A": left_eater(-23, -25),

        "B": [
            (10, -26),
            (11, -26),
            (11, -25),
            (8, -24),
            (9, -24),
            (10, -24),
            (8, -23)
        ],

        "OUT1": (4, 46),
        "OUT2": (-17, 46)
    }
}

# ============================================================
# INPUT CONTROL
# ============================================================

def remove_structure(cells):
    for x, y in cells:
        g.setcell(x, y, 0)

def set_input(gate, name, value):

    if value == 0:
        return

    remove_structure(
        GATES[gate][name]
    )

# ============================================================
# OUTPUT READ
# ============================================================

def read_output(gate):

    info = GATES[gate]

    if gate == "XOR":

        alive1 = g.getcell(*info["OUT1"])
        alive2 = g.getcell(*info["OUT2"])

        if alive1 and alive2:
            return 0
        else:
            return 1

    alive = g.getcell(*info["OUT"])

    if alive:
        return 0
    else:
        return 1

# ============================================================
# RUN GATE
# ============================================================

def run_gate(gate, A, B=None, steps=5000):

    g.open(GATES[gate]["file"])

    set_input(gate, "A", A)

    if B is not None:
        set_input(gate, "B", B)

    g.run(steps)

    return read_output(gate)

# ============================================================
# TEST ALL
# ============================================================

def test_and():
    print("AND")
    print("00 =", run_gate("AND", 0, 0))
    print("01 =", run_gate("AND", 0, 1))
    print("10 =", run_gate("AND", 1, 0))
    print("11 =", run_gate("AND", 1, 1))
    print()

def test_or():
    print("OR")
    print("00 =", run_gate("OR", 0, 0))
    print("01 =", run_gate("OR", 0, 1))
    print("10 =", run_gate("OR", 1, 0))
    print("11 =", run_gate("OR", 1, 1))
    print()

def test_xor():
    print("XOR")
    print("00 =", run_gate("XOR", 0, 0))
    print("01 =", run_gate("XOR", 0, 1))
    print("10 =", run_gate("XOR", 1, 0))
    print("11 =", run_gate("XOR", 1, 1))
    print()

def test_not():
    print("NOT")
    print("0 =", run_gate("NOT", 0))
    print("1 =", run_gate("NOT", 1))
    print()

# ============================================================
# MAIN
# ============================================================

test_and()
test_or()
test_xor()
test_not()