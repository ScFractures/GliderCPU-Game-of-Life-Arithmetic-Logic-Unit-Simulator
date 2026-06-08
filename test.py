import golly as g

# ============================================================
# eater
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
# gates
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
            (10,-26),(11,-26),(11,-25),
            (8,-24),(9,-24),(10,-24),(8,-23)
        ],
        "OUT1": (4, 46),
        "OUT2": (-17, 46)
    }
}

# ============================================================
# SAFE VISUAL LOG (THIS WORKS IN GOLLY 5.0)
# ============================================================

def log(msg):
    g.note(str(msg))
    g.show(str(msg))

# ============================================================
# CORE
# ============================================================

def remove(cells):
    for x, y in cells:
        g.setcell(x, y, 0)

def set_input(gate, name, value):
    if value == 0:
        return
    remove(GATES[gate][name])

def read_output(gate):

    info = GATES[gate]

    if gate == "XOR":
        a = g.getcell(*info["OUT1"])
        b = g.getcell(*info["OUT2"])
        return 1 if (not a or not b) else 0

    return 1 if not g.getcell(*info["OUT"]) else 0

def run_gate(gate, A, B=None, steps=5000):

    g.open(GATES[gate]["file"])

    set_input(gate, "A", A)
    if B is not None:
        set_input(gate, "B", B)

    g.run(steps)

    return read_output(gate)

# ============================================================
# TEST
# ============================================================

def test_gate(name):

    log("===== " + name + " =====")

    if name == "NOT":

        for A in [0,1]:
            res = run_gate(name, A)
            log("NOT(" + str(A) + ") = " + str(res))

    else:

        for A in [0,1]:
            for B in [0,1]:
                res = run_gate(name, A, B)
                log(name + "(" + str(A) + "," + str(B) + ") = " + str(res))

    log("===== DONE =====")

# ============================================================
# RUN
# ============================================================

test_gate("AND")
test_gate("OR")
test_gate("XOR")
test_gate("NOT")