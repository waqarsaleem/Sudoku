import functools
from colorama import Fore
from colorama import Style
import pdb

class Cell:
    def __init__(self):
        self.possibilities = set(range(1,10))
        self.value = None
        self.value_set_observers = []
        self.single_possibility_observers = []
        # TODO: change relevant attributes, e.g. value, to "property".

    def __repr__(self):
        if self.is_set():
            return f'{self.value}'
        return f'{self.possibilities}'
        
    def get(self):
        return self.value
    
    def is_set(self):
        # TODO: change is_set to property ?
        return bool(self.value)

    def set(self, value):
        assert 1 <= value <= 9
        self.value = value
        self.possibilities = None
        for callback in self.value_set_observers:
            callback(value)
            
    def add_possibility(self, value):
        if not self.is_set():
            self.possibilities.add(value)

    def remove_possibility(self, value):
        if not self.is_set():
            self.possibilities.discard(value)
            if len(self.possibilities) == 1:
                for callback in self.single_possibility_observers:
                    callback(next(iter(self.possibilities)))

    def bind_value_set_observer(self, f):
        self.value_set_observers.append(f)
        
    def bind_single_possibility_observer(self, f):
        self.single_possibility_observers.append(f)

class Board:
    def __init__(self):
        self.board = []
        for row_num in range(9):
            row = []
            for col_num in range(9):
                cell = Cell()
                row.append(cell)
            self.board.append(row)

    # TODO: make iterators for row and column
    def get_row_values(self, row_num):
        '''0-based row_num
        '''
        return [cell.get() for cell in self.board[row_num] if cell.is_set()]

    def get_column_values(self, col_num):
        '''0-based col_num
        '''
        # TODO: investigate assignment in list comprehension
        return [self.board[i][col_num].get() for i in range(9) \
                if self.board[i][col_num].is_set()]

    def get_block_values(self, block_num):
        '''0-based block_num from left to right and top to bottom.
        Top left block is numbered 1 and bottom right is numbered 9.
        '''
        start_row, start_col = [3*n for n in divmod(block_num, 3)]
        values = []
        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                if self.board[row][col].is_set():
                    values.append(self.board[row][col].get())
        return values

    def remove_row_possiblity(self, row_num, value):
        '''0-based row_num.
        '''
        # TODO: Idiomatic way to call method on all objects in a list.
        for cell in self.board[row_num]:
            cell.remove_possibility(value)

    def remove_column_possiblity(self, col_num, value):
        '''0-based col_num.
        '''
        # TODO: Idiomatic way to call method on all objects in a list.
        for i in range(9):
            self.board[i][col_num].remove_possibility(value)

    def remove_block_possiblity(self, block_num, value):
        '''0-based block_num.
        '''
        # TODO: Idiomatic way to call method on all objects in a list.
        start_row, start_col = [3*n for n in divmod(block_num, 3)]
        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                self.board[row][col].remove_possibility(value)

    def get_cell(self, row_num, col_num):
        '''0-based row_num and col_num.
        '''
        return self.board[row_num][col_num]

    def get_value(self, row_num, col_num):
        '''0-based row_num and col_num.
        '''
        return self.board[row_num][col_num].get()
        
    def set_cell(self, row_num, col_num, value):
        '''0-based row_num and col_num.
        '''
        assert 0 <= row_num < 9
        assert 0 <= col_num < 9
        if not self.board[row_num][col_num].is_set():
            self.board[row_num][col_num].set(value)
    
class Sudoku:
    def __init__(self):
        self.board = Board()
        self.observing = False
    
    def __repr__(self):
        string = ''
        possibilities = []
        counter = ['A', '1']
        def increment_counter():
            if counter[-1] == '9':
                counter[-1] = '0'
                counter[0] = chr(ord(counter[0]) + 1)
            else:
                counter[-1] = chr(ord(counter[-1]) + 1)
        for row in range(9):
            string += '-'*46 + '\n|'
            for col in range(9):
                cell = self.board.get_cell(row, col)
                s = ''
                if cell.is_set():
                    string += f'{cell.get():^4}|'
                else:
                    s = f'{counter[0]}{counter[1]}'
                    possibilities.append((s, cell.possibilities))
                    increment_counter()
                    string += f'{Fore.RED}{s:^4}{Style.RESET_ALL}|'
            string += '\n'
        string += '-'*46 + '\n'
        # TODO: pretty print possibilities
        string += f'\n{possibilities}'
        return string 
    
    def is_solved_row(self, row_num):
        '''0-based row_num
        '''
        # TODO: formulate in terms of "any".
        row_values = self.board.get_row_values(row_num)
        for i in range(1,10):
            if row_values.count(i) != 1:
                return False
        return True
    
    def is_solved_column(self, col_num):
        '''0-based col_num
        '''
        # TODO: formulate in terms of "any".
        col_values = self.board.get_column_values(col_num)
        for i in range(1,10):
            if col_values.count(i) != 1:
                return False
        return True
    
    def is_solved_block(self, block_num):
        '''0-based block_num
        '''
        # TODO: formulate in terms of "any".
        block_values = self.board.get_block_values(block_num)
        for i in range(1,10):
            if block_values.count(i) != 1:
                return False
        return True

    def is_solved(self):
        for i in range(9):
            if not self.is_solved_row(i):
                return False
            if not self.is_solved_column(i):
                return False
            if not self.is_solved_block(i):
                return False
        return True

    def set_cell(self, row_num, col_num, value):
        '''0-based row_num and col_num.
        '''
        self.board.set_cell(row_num, col_num, value)

    def add_observers(self):
        board = self.board
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                cell.bind_single_possibility_observer(cell.set)
                cell.bind_value_set_observer(
                    functools.partial(board.remove_row_possiblity, row))
                cell.bind_value_set_observer(
                    functools.partial(board.remove_column_possiblity, col))
                block = 3*(row//3) + (col//3)
                print(row, col, block)
                cell.bind_value_set_observer(
                    functools.partial(board.remove_block_possiblity, block))
        self.observing = True
        
    def solve(self):
        if not self.observing:
            if self.is_solved():
                return
            self.add_observers()
        for row in range(9):
            for col in range(9):
                if self.board.get_cell(row, col).is_set():
                    value = self.board.get_value(row, col)
                    self.board.remove_row_possiblity(row, value)
                    self.board.remove_column_possiblity(col, value)
                    block = 3*(row//3) + (col//3)
                    self.board.remove_block_possiblity(block, value)
        if not self.is_solved():
            self.solve()

def set_sample_board(sudoku):
    sudoku.set_cell(0,5,9)
    sudoku.set_cell(1,0,6)
    sudoku.set_cell(1,5,8)
    sudoku.set_cell(1,7,3)
    sudoku.set_cell(2,0,2)
    sudoku.set_cell(2,1,8)
    sudoku.set_cell(2,2,5)
    sudoku.set_cell(2,4,4)
    sudoku.set_cell(3,0,8)
    sudoku.set_cell(3,1,1)
    sudoku.set_cell(3,3,4)
    sudoku.set_cell(3,4,7)
    sudoku.set_cell(3,5,5)
    sudoku.set_cell(3,6,3)
    sudoku.set_cell(3,8,6)
    sudoku.set_cell(4,1,9)
    sudoku.set_cell(4,4,3)
    sudoku.set_cell(4,5,1)
    sudoku.set_cell(4,8,5)
    sudoku.set_cell(5,0,3)
    sudoku.set_cell(5,1,5)
    sudoku.set_cell(5,2,4)
    sudoku.set_cell(5,3,2)
    sudoku.set_cell(5,6,8)
    sudoku.set_cell(5,7,7)
    sudoku.set_cell(5,8,1)
    sudoku.set_cell(6,0,4)
    sudoku.set_cell(6,2,8)
    sudoku.set_cell(6,3,3)
    sudoku.set_cell(6,4,1)
    sudoku.set_cell(6,8,9)
    sudoku.set_cell(7,0,9)
    sudoku.set_cell(7,1,3)
    sudoku.set_cell(7,4,5)
    sudoku.set_cell(7,5,7)
    sudoku.set_cell(7,8,2)
    sudoku.set_cell(8,0,5)
    sudoku.set_cell(8,3,9)
    sudoku.set_cell(8,4,8)
    sudoku.set_cell(8,6,6)
    sudoku.set_cell(8,8,3)
    
sudoku = Sudoku()
set_sample_board(sudoku)
