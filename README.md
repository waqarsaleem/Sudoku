# Sudoku Solver

This is a program to solve a [Sudoku](https://en.wikipedia.org/wiki/Sudoku) puzzle. The entire program is in the file `sudoku.py`.

To use the program,

1. initialize a new `Sudoku` instance,
```
sudoku = Sudoku()
```
2. enter initial values. An example is provided in the `set_sample_board` function,
```
set_sample_board(sudoku)
```
3. call the `solve` method on the instance.
```
sudoku.solve()
```

The first 2 steps are illustrated toward the bottom of the file. The instance can be printed at any time.

## Requirements

- Python `f-strings` are used liberally. These are introduced in Python 3.6 so you will need a Python distribution which is at least 3.6.
- Printing requires the `colorama` package which may need to be installed seaprately, `pip install colorama` or `pip3 install colorama` depending on your platform.

## How it Works

The puzzle is solved by pruning _possibilities_.  Each cell has 9 possiblities by default - 1 to 9. Some cells are _set_ to a particular number which is the cell's _value_. They have no possiblity. Each puzzle usually has some _set_ cells in the beginning. The following strategy is applied until the puzzle is solved.

1. For each cell that is set, remove its value from the set of possibiltiies of all cells in the same row, column, and block.
1. Set cells that have only one remaining possibility to a value equal to that possibility.

The puzzle is solved when every row, column, and block contains only 1 occurrence of each number from 1 to 9.

## Code Details

The code models a `Cell`. A `Board` is a 9x9 grid of `Cell` instances. The 9 rows are numberd 0 to 8 from top to bottom and the 9 columns are numbered 0 to 8 from left to right. A `Sudoku` is essentially a `Board` with certain rules enforced on it. The [_Observer pattern_](https://stackoverflow.com/questions/6190468/how-to-trigger-function-on-value-change) is used to implement the logic above. This is in the form of a list of `observer`s in `Cell` which are _bound_ in the `Sudoku` class.

## Contributions

- _Documentation_. The code needs to be perused, understood, and meaingfully documented.
- _Best practices_. Some code can be replaced with python best practices like
    - [`property`](https://www.programiz.com/python-programming/property), 
	- replacing `range` in `for` loops with custom iterables, as described in [this PyCon 2017 talk](https://youtu.be/u8g9scXeAcI).
	- Simplify some of the code in a more idiomatic manner.
	- Many of these are listed in the code as _TODO_s.
- _Unit tests_. To verify the correctness of the code.
- _Board initialization_. A more convenient way to intialize the board. Currently each cell is initialized individually, as in `set_sample_board`.
- _Miscellaneous_. Any other  _TODO_s in the code.
- _Adding strategies_ (HARD). There is currently only one strategy and it is hardcoded. We would like to be able to encode various strategies and choose which ones to apply. The [_Strategy Pattern_](https://en.wikipedia.org/wiki/Strategy_pattern) may help, at least the name implies so!
- _GUI_ (HARD). A GUI implemntation.
- _Other_. Any other useful features you can think of.
