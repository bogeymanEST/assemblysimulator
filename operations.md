#Operations
##Add
`Add a, b, dest`


Adds a and b and stores the result in the destination.

`a` - The source of the first value

`b` - The source of the second value (default = accumulator)

`dest` - The destination (default = b)

Examples:

```
Add R1, 25
```

##And
`And a, b, dest`


Performs the logical AND operation on the binary representation of the given values and stores it in the destination
`a` - The first value

`b` - The second value (default = accumulator)

`dest` - The destination (default = b)

Examples:

```
```

##AshiftL
`AshiftL num, dest`

`num` - 

`dest` - 

##AshiftR
`AshiftR num, dest`

`num` - 

`dest` - 

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
`LshiftL num, dest`

`num` - 

`dest` - 

##Multiply
`Multiply src, dest`

`src` - 

`dest` - 

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
Load #%1100 R1 ;Load binary 1100 into R1
Not R1 ;Accumulator now contains 0011
Load R1 ;Load the value of the accumulator into R1
```

##RotateL
`RotateL num, dest`

`num` - 

`dest` - 

##RotateLC
`RotateLC num, dest`

`num` - 

`dest` - 

##RotateR
`RotateR num, dest`

`num` - 

`dest` - 

##RotateRC
`RotateRC num, dest`

`num` - 

`dest` - 

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

##lshiftR
`lshiftR num, dest`

`num` - 

`dest` - 

