#Operations
##Add
`Add a, b, dest`


Adds a and b and stores the result in the destination.


`a` - The source of the first value

`b` - The source of the second value (default = accumulator)

`dest` - The destination (default = b)

Examples:

```
Add R1, 25 ;Add the value of R1 to the value of memory slot 25 and store it in the same memory slot
```

```
Add #4 ;Add 4 to the value of the accumulator
```

##And
`And a, b, dest`


Performs the logical AND operation on the binary representation of the given values and stores it in the destination

`a` - The first value

`b` - The second value (default = accumulator)

`dest` - The destination (default = b)

Examples:

```
Load #%1001, R1 ;Load binary 1001 into R1
And #%1100, R1 ;Perform the AND operation and store the result in R1 (now contains binary 1000)
```

##AshiftL
`AshiftL num, val, dest`


Performs the logical left shift on the binary representation of the given value.

`num` - The number of shifts to do

`val` - The value to shift

`dest` - The destination to save the result to (default = val)

##AshiftR
`AshiftR num, val, dest`


Performs the artihmetic right shift on the binary representation of the given value.

`num` - The number of bits to shift

`val` - The value to shift

`dest` - The destination to save the result to (default = val)

##Branch!=0
`Branch!=0 dest`


If the value of the last operation is not equal to 0, jump the program execution to the given line.

`dest` - The line to jump to (lines are numbered from 0, each line number increasing by the word size)

##Branch<0
`Branch<0 dest`


If the value of the last operation is less than 0, jump the program execution to the given line.

`dest` - The line to jump to (lines are numbered from 0, each line number increasing by the word size)

##Branch=0
`Branch=0 dest`


If the value of the last operation is equal to 0, jump the program execution to the given line.

`dest` - The line to jump to (lines are numbered from 0, each line number increasing by the word size)

##Branch>0
`Branch>0 dest`


If the value of the last operation is greater than 0, jump the program execution to the given line.

`dest` - The line to jump to (lines are numbered from 0, each successive line number increasing by the word size)

Examples:

```
Load #13, R2 ;Set result to 13
Load #4, R1 ;Set the number of loops
Add #3, R2 ;Add 3 to the result
Increment R1 ;Add 1 to the loop counter
Branch>0 8 ;Jump to the "Add ..." line if R1 is greater than 0.
Load 123, R1 ;Memory slot 123 now contains the result of the additions (13 + 3 * 4)
```

##Clear
`Clear loc`


Clears the given value

`loc` - The value to clear (default = accumulator)

Examples:

```
Clear (R1) ;Clear the memory slot pointed to by R1
```

```
Clear ;Clear the accumulator
```

##Decrement
`Decrement a`


Decrease the given value by one.

`a` - The value to decrement (default = accumulator)

Examples:

```
Load #15 ;Set the value of the accumulator to 15
Decrement ;Accumulator is now 14
```

##Increment
`Increment a`


Increase the given value by one.

`a` - The value to increment (default = accumulator)

Examples:

```
Load #4, R1 ;Set R1 to 4
Increment R1 ;R1 is now 5
```

##Load
`Load src, dest`


Loads the source data into the destination.


`src` - The source of the data

`dest` - The destination to load the data into (default = accumulator)

Examples:

```
Load 44 ;Loads the value of memory slot 44 into the accumulator
```

```
Load #45, R1 ;Loads the decimal number into registry R1
```

##LshiftL
`LshiftL num, val, dest`


Performs the logical left shift on the binary representation of the given value.

`num` - The number of shifts to do

`val` - The value to shift

`dest` - The destination to save the result to (default = val)

##LshiftR
`LshiftR num, val, dest`


Performs the logical right shift on the binary representation of the given value.

`num` - The number of shifts to do

`val` - The value to shift

`dest` - The destination to save the result to (default = val)

##Multiply
`Multiply a, b, dest`


Multiplies two values and stores the result in the destination value.

`a` - The first value

`b` - The second value (default = accumulator)

`dest` - The destination to save the result to (default = b)

Examples:

```
Multiply #5 ;Multiplies the value of the accumulator by 5
```

```
Multiply R1, #4, R2 ;Multiplies the value of R1 by 4 and stores the result in R2
```

##Not
`Not src, dest`


Performs the logical NOT operation on the binary representation of the given value and stores it in the destination

`src` - The source value

`dest` - The destination (default = accumulator)

Examples:

```
Load #%1010 R1 ;Load binary 1010 into R1
Not R1, R1 ;R1 now contains 0101
```

```
Load #%1100, R1 ;Load binary 1100 into R1
Not R1 ;Accumulator now contains 0011
Load R1 ;Load the value of the accumulator into R1
```

##RotateL
`RotateL num, val, dest`


Rotates the binary representation of the given value to the left

`num` - Number of bits to rotate

`val` - The value to rotate

`dest` - The destination to save the result to (default = val)

##RotateLC
`RotateLC num, val, dest`


Rotates the binary representation of the given value to the left taking into account the carry bit.

`num` - Number of bits to rotate

`val` - The value to rotate

`dest` - The destination to save the result to (default = val)

##RotateR
`RotateR num, val, dest`


Rotates the binary representation of the given value to the right

`num` - Number of bits to rotate

`val` - The value to rotate

`dest` - The destination to save the result to (default = val)

##RotateRC
`RotateRC num, val, dest`


Rotates the binary representation of the given value to the right taking into account the carry bit.

`num` - Number of bits to rotate

`val` - The value to rotate

`dest` - The destination to save the result to (default = val)

##Store
`Store dest`


Sets the value of the destination to the value of the accumulator

`dest` - The destination

Examples:

```
Clear ;Clear the accumulator
Add #4 ;Add 4 to the accumulator
Add #5 ;Add 5 to the accumulator
Store R1 ;R1 now contains 9
```

