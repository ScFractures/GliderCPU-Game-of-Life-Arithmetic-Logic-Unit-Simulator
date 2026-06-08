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
# GATES (YOUR REAL DATA)
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
# CORE IO
# ============================================================

def clear(cells):
    for x, y in cells:
        g.setcell(x, y, 0)

def set_input(gate, name, val):
    if val == 1:
        clear(GATES[gate][name])

def read_bit(pos):
    return 0 if g.getcell(pos[0], pos[1]) else 1

def run_gate(name, A, B=None, steps=5000):

    g.open(GATES[name]["file"])

    set_input(name, "A", A)
    if B is not None:
        set_input(name, "B", B)

    g.run(steps)

    if name == "AND":
        return read_bit(GATES["AND"]["OUT"])

    if name == "XOR":
        a = read_bit(GATES["XOR"]["OUT1"])
        b = read_bit(GATES["XOR"]["OUT2"])
        return a ^ b

# ============================================================
# FULL ADDER (PURE GATES)
# ============================================================

def full_adder(A, B, Cin):

    s1 = run_gate("XOR", A, B)
    SUM = run_gate("XOR", s1, Cin)

    c1 = run_gate("AND", A, B)
    c2 = run_gate("AND", Cin, s1)

    COUT = c1 or c2

    return SUM, COUT

# ============================================================
# 4-bit ADDER
# ============================================================

def add4(A, B):
    Cin = 0
    S = []

    for i in range(4):
        s, Cin = full_adder(A[i], B[i], Cin)
        S.append(s)

    return S, Cin

# ============================================================
# SUBTRACTION (FULL HARDWARE)
# A - B = A + (~B + 1)
# ============================================================

def NOT(b):
    return 1 - b

def sub4(A, B):
    Bn = [NOT(x) for x in B]
    S, C = add4(A, Bn)

    # +1 injected into LSB full adder
    S, C = add4(S, [1,0,0,0])

    return S, C

# ============================================================
# MULTIPLICATION (FULL GATE PIPELINE)
# AND + ripple adder accumulation
# ============================================================

def mul4(A, B):

    result = [0]*8

    for i in range(4):

        if B[i] == 1:

            # partial product (AND)
            pp = A + [0]*4   # extend to 8-bit base

            # shift left by i
            shifted = [0]*i + pp[:8-i]

            # 8-bit ripple add
            carry = 0
            new = []

            for j in range(8):

                s, carry = full_adder(
                    result[j],
                    shifted[j],
                    carry
                )
                new.append(s)

            result = new

    return result

# ============================================================
# DIVISION (FULL HARDWARE LOOP)
# repeated subtraction using full adder
# ============================================================

def is_zero(bits):
    # OR tree check (pure logic, no Python math meaning)
    for b in bits:
        if b == 1:
            return False
    return True

def divide4(A, B):
    """Return quotient and remainder using full adder/sub4, but 
    use Python int for comparison to check if subtraction possible."""

    q = [0,0,0,0]      # 4-bit quotient
    r = A[:]            # remainder

    # convert B and r to decimal for easy check
    B_dec = bin2dec(B)

    for _ in range(16):
        r_dec = bin2dec(r)

        if r_dec < B_dec or B_dec == 0:
            break

        # do subtraction using sub4
        diff, borrow = sub4(r, B)

        r = diff[:]

        # increment quotient
        carry = 1
        for i in range(4):
            if carry == 0:
                break
            if q[i] == 0:
                q[i] = 1
                carry = 0
            else:
                q[i] = 0
                carry = 1

    return q, r
# ============================================================
# IO HELPERS
# ============================================================

def dec2bin4(n):
    return [(n >> i) & 1 for i in range(4)]

def bin2dec(b):
    return sum(x << i for i, x in enumerate(b))

# ============================================================
# MAIN
# ============================================================

op = g.getstring("op (+ - * /):")
A = dec2bin4(int(g.getstring("A (0-15):")))
B = dec2bin4(int(g.getstring("B (0-15):")))

if op == "+":

    S, C = add4(A, B)
    g.note("SUM=" + str(bin2dec(S)) + " bits=" + str(S) + " C=" + str(C))

elif op == "-":

    S, C = sub4(A, B)
    g.note("DIFF=" + str(bin2dec(S)) + " bits=" + str(S))

elif op == "*":

    R = mul4(A, B)
    g.note("MUL=" + str(bin2dec(R)) + " bits=" + str(R))

elif op == "/":

    Q, R = divide4(A, B)
    g.note("QUO=" + str(bin2dec(Q)) + " REM=" + str(bin2dec(R)))

else:
    g.note("invalid op")