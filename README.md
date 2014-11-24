
assemblysimulator
=================

A simple simulator of assembly instructions.

#Running
All necessary configuration is done using the `initialize` method.

Example initialization:
```Python
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
```
Use `run_string` to run the program (supports multiline strings):
```Python
run_string("""
Load #1204, R1
Add (R1),(R2),R5
""")
```

#Pointers
Here is a table of the ways values can be pointed to.

Example | Meaning
-------| -------
\#123 | The decimal value 123
\#%0101 | The binary value 0101
\#$3F | The hexadecimal value 3F
341 | The value of the memory block at address 341
R3 | The value of registry 3
(567) | The value of the memory block at the stored at memory address 567
(R2) | The value of the memory at the address stored in registry 2
(R1)+ | Return the value of the memory at the address stored in R1 and increment the value of R1 by one word (default 4 bytes)
-(245) | Decrement the value of memory block 245 by one word and return the memory block value at the address stored in memory block 245


#Operations
Click [https://github.com/bogeymanEST/assemblysimulator/blob/master/operations.md](here) for the complete list of operations.