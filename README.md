
assemblysimulator
=================

A simple simulator of assembly instructions.

#Running
All necessary configuration is done using the `initialize` method.

Example initialization:
```Python
initialize(
    # Registry values
    reg={
        "R1": 0b11110110,
        "R2": 3240,
        "R5": 2032
    },

    # Memory values
    mem={
        "1204": 3240,
        "3240": 508
    },

    # Stack pointer
    sp=Value(),

    # Carry bit
    c="1"
)
```
Use `run_string` to run the program (supports multiline strings):
```Python
run_string("""
Load #1204, R1
Add (R1),(R2),R5
""")
```

##Initialization options
 * reg - A dictionary containing the initial values to the registries. There is no limit to the number of registries you can add.
 * mem - A dictionary mapping memory locations to their initial values. There is no limit to the number of memory locations.
 * sp - The initial value of the stack pointer
 * c - The carry bit (either "1" or "0")

#Syntax
A program consists of a number of lines. Each operation is on its own line. Operation arguments are separated by commas.

Comments can be written after operations and they start with a semicolon and continue until the end of the line.

#Pointers
Here is a table of the ways values can be pointed to.

Example | Meaning
-------| -------
\#123 | The decimal value 123
\#%0101 | The binary value 0101
\#$3F | The hexadecimal value 3F
341 | The value of the memory block at address 341
R3 | The value of registry 3
SP | The value of the stack pointer
(567) | The value of the memory block at the stored at memory address 567
(R2) | The value of the memory at the address stored in registry 2
(R1)+ | Return the value of the memory at the address stored in R1 and increment the value of R1 by one word (default 4 bytes)
-(245) | Decrement the value of memory block 245 by one word and return the memory block value at the address stored in memory block 245


#Operations
All operation names are case-insensitive

Click [here](https://github.com/bogeymanEST/assemblysimulator/blob/master/operations.md) for a complete list of operations.