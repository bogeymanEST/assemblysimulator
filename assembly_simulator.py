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
    """
    Loads the source data into the destination.

    :param src: The source of the data
    :param dest: The destination to load the data into (default = accumulator)
    :example:
    Load 44 ;Loads the value of memory slot 44 into the accumulator
    :example:
    Load #45, R1 ;Loads the decimal number into registry R1
    """
    dest.value = src.value
    result.value = dest.value


def add(a, b=accumulator, dest=None):
    """
    Adds a and b and stores the result in the destination.

    :param a: The source of the first value
    :param b: The source of the second value (default = accumulator)
    :param dest: The destination (default = b)
    :example:
    Add R1, 25 ;Add the value of R1 to the value of memory slot 25 and store it in the same memory slot
    :example:
    Add #4 ;Add 4 to the value of the accumulator
    """
    if dest is None:
        dest = b
    dest.value = a.value + b.value
    result.value = dest.value


def store(dest):
    """
    Sets the value of the destination to the value of the accumulator
    :param dest: The destination
    :example:
    Clear ;Clear the accumulator
    Add #4 ;Add 4 to the accumulator
    Add #5 ;Add 5 to the accumulator
    Store R1 ;R1 now contains 9
    """
    dest.value = accumulator.value
    result.value = dest.value


def increment(a=accumulator):
    """
    Increase the given value by one.
    :param a: The value to increment (default = accumulator)
    :example:
    Load #4, R1 ;Set R1 to 4
    Increment R1 ;R1 is now 5
    """
    a.value += 1
    result.value = a.value


def decrement(a=accumulator):
    """
    Decrease the given value by one.
    :param a: The value to decrement (default = accumulator)
    :example:
    Load #15 ;Set the value of the accumulator to 15
    Decrement ;Accumulator is now 14
    """
    a.value -= 1
    result.value = a.value


def branch_g0(dest):
    """
    If the value of the last operation is greater than 0, jump the program execution to the given line.
    :param dest: The line to jump to (lines are numbered from 0, each successive line number increasing by the word size)
    :example:
    Load #13, R2 ;Set result to 13
    Load #4, R1 ;Set the number of loops
    Add #3, R2 ;Add 3 to the result
    Increment R1 ;Add 1 to the loop counter
    Branch>0 8 ;Jump to the "Add ..." line if R1 is greater than 0.
    Load 123, R1 ;Memory slot 123 now contains the result of the additions (13 + 3 * 4)
    """
    global counter
    if result.value > 0:
        counter.value = dest.value


def branch_l0(dest):
    """
    If the value of the last operation is less than 0, jump the program execution to the given line.
    :param dest: The line to jump to (lines are numbered from 0, each line number increasing by the word size)
    """
    global counter
    if result.value < 0:
        counter.value = dest.value


def branch_e0(dest):
    """
    If the value of the last operation is equal to 0, jump the program execution to the given line.
    :param dest: The line to jump to (lines are numbered from 0, each line number increasing by the word size)
    """
    global counter
    if result.value == 0:
        counter.value = dest.value


def branch_ne0(dest):
    """
    If the value of the last operation is not equal to 0, jump the program execution to the given line.
    :param dest: The line to jump to (lines are numbered from 0, each line number increasing by the word size)
    """
    global counter
    if result.value != 0:
        counter.value = dest.value


def clear(loc=accumulator):
    """
    Clears the given value
    :param loc: The value to clear (default = accumulator)
    :example:
    Clear (R1) ;Clear the memory slot pointed to by R1
    :example:
    Clear ;Clear the accumulator
    """
    loc.value = 0
    result.value = 0


def not_cmd(src, dest=None):
    """
    Performs the logical NOT operation on the binary representation of the given value and stores it in the destination
    :param src: The source value
    :param dest: The destination (default = accumulator)
    :example:
    Load #%1010 R1 ;Load binary 1010 into R1
    Not R1, R1 ;R1 now contains 0101
    :example:
    Load #%1100, R1 ;Load binary 1100 into R1
    Not R1 ;Accumulator now contains 0011
    Load R1 ;Load the value of the accumulator into R1
    """
    if dest is None:
        dest = src
    dest.set_binary("".join("1" if n == "0" else "0" for n in src.get_binary()))
    result.value = dest.value


def and_cmd(a, b, dest=None):
    """
    Performs the logical AND operation on the binary representation of the given values and stores it in the destination
    :param a: The first value
    :param b: The second value (default = accumulator)
    :param dest: The destination (default = b)
    :example:
    Load #%1001, R1 ;Load binary 1000 into R1
    And #%1100, R1 ;Perform the AND operation and store the result in R1 (now contains binary 1000)
    """
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


def lshiftl(num, val, dest=None):
    """
    Performs the logical left shift on the binary representation of the given value.
    :param num: The number of shifts to do
    :param val: The value to shift
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
    d_bin = val.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[1:] + "0"
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def lshiftr(num, val, dest=None):
    """
    Performs the logical right shift on the binary representation of the given value.
    :param num: The number of shifts to do
    :param val: The value to shift
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
    d_bin = val.get_binary()
    c = 0
    while c < num.value:
        d_bin = "0" + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def ashiftr(num, val, dest=None):
    """
    Performs the artihmetic right shift on the binary representation of the given value.
    :param num: The number of bits to shift
    :param val: The value to shift
    :param dest: The destination to save the result to (default = val)
    """
    d_bin = val.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[0] + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotatel(num, val, dest=None):
    """
    Rotates the binary representation of the given value to the left
    :param num: Number of bits to rotate
    :param val: The value to rotate
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
    d_bin = val.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[1:] + d_bin[0]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotater(num, val, dest):
    """
    Rotates the binary representation of the given value to the right
    :param num: Number of bits to rotate
    :param val: The value to rotate
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
    d_bin = dest.get_binary()
    c = 0
    while c < num.value:
        d_bin = d_bin[len(d_bin) - 1] + d_bin[0:len(d_bin) - 1]
        c += 1
    dest.set_binary(d_bin)
    result.value = dest.value


def rotatelc(num, val, dest=None):
    """
    Rotates the binary representation of the given value to the left taking into account the carry bit.
    :param num: Number of bits to rotate
    :param val: The value to rotate
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
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


def rotaterc(num, val, dest=None):
    """
    Rotates the binary representation of the given value to the right taking into account the carry bit.
    :param num: Number of bits to rotate
    :param val: The value to rotate
    :param dest: The destination to save the result to (default = val)
    """
    if dest is None:
        dest = val
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


def multiply(a, b=accumulator, dest=None):
    """
    Multiplies two values and stores the result in the destination value.
    :param a: The first value
    :param b: The second value (default = accumulator)
    :param dest: The destination to save the result to (default = b)
    """
    if dest is None:
        dest = b
    dest.value = a.value * b.value
    result.value = dest.value


commands = {
    "Load": load,
    "Add": add,
    "Store": store,
    "Decrement": decrement,
    "Increment": increment,
    "Branch>0": branch_g0,
    "Branch<0": branch_l0,
    "Branch=0": branch_e0,
    "Branch!=0": branch_ne0,
    "Clear": clear,
    "Not": not_cmd,
    "And": and_cmd,
    "LshiftL": lshiftl,
    "lshiftR": lshiftr,
    "AshiftR": ashiftr,
    "AshiftL": lshiftl,
    "RotateL": rotatel,
    "RotateR": rotater,
    "RotateLC": rotatelc,
    "RotateRC": rotaterc,
    "Multiply": multiply,
}

pretty_commands = commands

commands = {k.lower(): v for k, v in commands.items()}
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


if __name__ == '__main__':
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

