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
# gates (reuse your working ones)
# ============================================================

GATES = {

    "AND": {
        "file": "and_gate.rle",
        "A": left_eater(-41, -20),
        "B": left_eater(5, -21),
        "OUT": (17, 35)
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
# safe log
# ============================================================

def log(msg):
    g.note(str(msg))
    g.show(str(msg))

# ============================================================
# core
# ============================================================

def remove(cells):
    for x, y in cells:
        g.setcell(x, y, 0)

def set_input(gate, name, value):
    if value == 0:
        return
    remove(GATES[gate][name])

def read_AND():
    x, y = GATES["AND"]["OUT"]
    return 1 if not g.getcell(x, y) else 0

def read_XOR():
    a = g.getcell(*GATES["XOR"]["OUT1"])
    b = g.getcell(*GATES["XOR"]["OUT2"])
    return 1 if (not a or not b) else 0

def run_gate(name, A, B, steps=5000):

    g.open(GATES[name]["file"])

    set_input(name, "A", A)
    set_input(name, "B", B)

    g.run(steps)

    if name == "AND":
        return read_AND()
    else:
        return read_XOR()

# ============================================================
# FULL ADDER
# ============================================================

def full_adder(A, B, Cin):

    # sum = A XOR B XOR Cin
    s1 = run_gate("XOR", A, B)
    SUM = run_gate("XOR", s1, Cin)

    # carry = (A AND B) OR (Cin AND (A XOR B))
    c1 = run_gate("AND", A, B)
    c2 = run_gate("AND", Cin, s1)

    CARRY = 1 if (c1 or c2) else 0

    return SUM, CARRY

# ============================================================
# 1-bit full adder test
# ============================================================

log("===== FULL ADDER =====")

for A in [0,1]:
    for B in [0,1]:
        for Cin in [0,1]:

            s, c = full_adder(A, B, Cin)

            log(f"A={A} B={B} Cin={Cin} -> S={s} C={c}")

# ============================================================
# 4-bit ripple adder
# ============================================================

log("===== 4-BIT ADDER =====")

def add4(A_bits, B_bits):

    Cin = 0
    result = []

    for i in range(4):

        s, Cin = full_adder(A_bits[i], B_bits[i], Cin)
        result.append(s)

    return result, Cin


# example test: 1011 + 0110

A = [1,0,1,1]
B = [0,1,1,0]

S, Cout = add4(A, B)

log("A=" + str(A))
log("B=" + str(B))
log("SUM=" + str(S))
log("COUT=" + str(Cout))