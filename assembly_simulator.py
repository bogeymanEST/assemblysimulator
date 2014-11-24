import re
import inspect


# Data
class Value:
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return str(self.value) + "(0b%s)" % self.get_binary()

    def set_binary(self, binary):
        self.value = int(binary, base=2)

    def get_width(self):
        return len(bin(self.value)) - 2

    def get_binary(self, width=8):
        if width > 0:
            return bin(self.value)[2:].rjust(width, "0")
        return bin(self.value)[2:]

    def __add__(self, other):
        self.value += other

    def __sub__(self, other):
        self.value -= other


class LocatableValue(Value):
    def __init__(self, location, value=0):
        super().__init__(value)
        self.location = location

    def __repr__(self):
        return str(self.location) + " = " + super().__repr__()


# Settings
WORD_SIZE = 4  # The size of the word unit in bytes
counter = Value()
accumulator = Value()
result = Value()
stackpointer = Value()
carry = "0"
registries = []
memory = []

DEBUG = False

# Commands
def load(src, dest=accumulator):
    dest.value = src.value
    result.value = dest.value


def add(a, b=accumulator, dest=None):
    if dest is None:
        dest = b
    dest.value = a.value + b.value
    result.value = dest.value


def store(dest):
    dest.value = accumulator.value
    result.value = dest.value


def increment(a):
    a.value += 1
    result.value = a.value


def decrement(a):
    a.value -= 1
    result.value = a.value


def branch_g0(dest):
    global counter
    if result.value > 0:
        counter.value = dest.value


def branch_l0(dest):
    global counter
    if result.value < 0:
        counter.value = dest.value


def branch_e0(dest):
    global counter
    if result.value == 0:
        counter.value = dest.value


def branch_ne0(dest):
    global counter
    if result.value != 0:
        counter.value = dest.value


def clear(loc):
    loc.value = 0
    result.value = 0


def not_cmd(src, dest=accumulator):
    dest.set_binary("".join("1" if n == "0" else "0" for n in src.get_binary()))
    result.value = dest.value


def and_cmd(a, b=accumulator, dest=None):
    if dest is None:
        dest = b
    width = max(a.get_width(), b.get_width())
    a_bin = a.get_binary(width)
    b_bin = b.get_binary(width)
    dest.set_binary(
        "".join(
            "1" if a_bin[i] == b_bin[i] == "1" else "0"
            for i in range(width)
        )
    )
    result.value = dest.value


def lshiftl(num, dest):
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[1:] + "0"
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def lshiftr(num, dest):
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = "0" + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def ashiftr(num, dest):
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[0] + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotatel(num, dest):
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[1:] + d_bin[0]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotater(num, dest):
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[len(d_bin) - 1] + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotatelc(num, dest):
    global carry
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        rem = carry
        carry = d_bin[0]
        d_bin = d_bin[1:] + rem
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotaterc(num, dest):
    global carry
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        rem = carry
        carry = d_bin[len(d_bin) - 1]
        d_bin = rem + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def multiply(src, dest=accumulator):
    dest.value *= src.value
    result.value = dest.value


commands = {
    "load": load,
    "add": add,
    "store": store,
    "decrement": decrement,
    "increment": increment,
    "branch>0": branch_g0,
    "branch<0": branch_l0,
    "branch=0": branch_e0,
    "branch!=0": branch_ne0,
    "clear": clear,
    "not": not_cmd,
    "and": and_cmd,
    "lshiftl": lshiftl,
    "lshiftr": lshiftr,
    "ashiftr": ashiftr,
    "ashiftl": lshiftl,
    "rotatel": rotatel,
    "rotater": rotater,
    "rotatelc": rotatelc,
    "rotaterc": rotaterc,
    "multiply": multiply,
}


# Debug print
def d(*args):
    if DEBUG:
        print("[DEBUG]", *args)


def find_memory(loc):
    global memory
    m = [m for m in memory if m.location == str(loc)]
    if len(m) == 0:
        m = LocatableValue(str(loc))
        memory.append(m)
    else:
        m = m[0]
    return m


def find_registry(loc):
    global registries
    m = [m for m in registries if m.location == str(loc)]
    if len(m) == 0:
        return None
    m = m[0]
    return m


def set_memory(loc, value):
    mem = find_memory(loc)
    mem.value = value


def evaluate(v):
    d("Eval argument:", v)

    m = re.match("^#(\\d+)$", v)
    if m:
        d("Decimal value")
        return Value(int(m.group(1)))

    m = re.match("^#%([01]+)$", v)
    if m:
        d("Binary value")
        return Value(int(m.group(1), base=2))

    m = re.match("^#%([0-9A-F]+)$", v)
    if m:
        d("Hexadecimal value")
        return Value(int(m.group(1), base=16))
    m = re.match("^(R\\d+)$", v)
    if m:
        d("Value from registry")
        return find_registry(m.group(1))

    m = re.match("^(\\d+)$", v)
    if m:
        d("Value from memory")
        return find_memory(m.group(1))
    m = re.match("^SP$", v)
    if m:
        d("Value from stack pointer")
        return stackpointer.value

    m = re.match("^\\((.+)\\)$", v)
    if m:
        d("Indirect memory value")
        return find_memory(evaluate(m.group(1)).value)

    m = re.match("^\\((.+)\\)\\+$", v)
    if m:
        d("Indirect memory value with autoincrement")
        r = evaluate(m.group(1))
        v = find_memory(r.value)
        r.value += WORD_SIZE
        return v

    m = re.match("^-\\((.+)\\)$", v)
    if m:
        d("Indirect memory value with autodecrement")
        r = evaluate(m.group(1))
        r.value -= WORD_SIZE
        v = find_memory(r.value)
        return v
    return None


def run_lines(lines):
    global counter, commands
    while counter.value < len(lines) * WORD_SIZE:
        line = lines[counter.value // WORD_SIZE]
        counter.value += WORD_SIZE
        line = line.strip()
        d("Read command: " + line)
        sp = line.split(maxsplit=1)
        cmdname = sp[0].lower()
        if cmdname not in commands:
            raise RuntimeWarning(line + " - invalid command")
        cmd = commands[cmdname]
        args = sp[1].replace(" ", "").split(";")[0].split(",")
        spec = inspect.getargspec(cmd)
        if len(spec[0]) - len(spec[3] or []) > len(args):
            raise RuntimeWarning(line + "not enough arguments")
        args_eval = list(map(evaluate, args))
        if None in args_eval:
            raise RuntimeWarning(line + " - failed to evaluate argument(s) " + ",".join(
                [args[i] for i in range(len(args_eval)) if args_eval[i] == None]))
        d(cmdname + "(" + ", ".join(map(str, args_eval)) + ")")
        cmd(*args_eval)
        d("")


def print_status():
    global memory, registries, counter
    print("Program counter =", counter)
    print("Accumulator =", accumulator)
    print("Memory:")
    for m in sorted(memory, key=lambda x: x.location):
        print(m)
    print("Registries:")
    for r in sorted(registries, key=lambda x: x.location):
        print(r)


def init_memory(**kwargs):
    global memory
    memory = []
    for k, v in kwargs.items():
        memory.append(LocatableValue(k, v))


def init_registry(**kwargs):
    global registries
    registries = []

    for k, v in kwargs.items():
        registries.append(LocatableValue(k, v))


def initialize(reg=None, mem=None, sp=Value(), c="0"):
    global stackpointer, carry
    if not reg:
        reg = {}
    if not mem:
        mem = {}
    init_registry(**reg)
    init_memory(**mem)
    stackpointer.value = sp
    carry = c


def run_string(s):
    print("Current program:")
    print(s)
    print("=== STATUS BEFORE RUNNING ===")
    print_status()
    print()
    print("Running...")
    ret = run_lines(s.strip().split("\n"))
    print()
    print("=== STATUS AFTER RUNNING ===")
    print_status()
    return ret


initialize(
    # Registry values
    {
        "R1": 0b11110110,
        "R2": 3240,
        "R5": 2032
    },

    # Memory values
    {
        "1204": 3240,
        "3240": 508
    },

    # Stack pointer
    sp=Value(),

    # Carry bit
    c="1"
)
run_string(
"""
Load #1204, R1
Add (R1),(R2),R5
"""
)

