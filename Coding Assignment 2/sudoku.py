#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"


class Var(object):
    def __init__(self, pos):
        self.pos = pos  # 'A1', 'A2', ... , 'I9'
        self.legal_val = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __gt__(self, other):
        return len(self.legal_val) > len(other.legal_val) # to make 'MRV_variable = min(unassigned_variables)' works


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solved_board = backtrack(board)
    return solved_board


def backtrack(board):
    # check if assignment is complete
    if (0 not in board.values()): return board

    variable = select_unassigned_variables(board)

    for val in variable.legal_val:
        board[variable.pos] = val
        result = backtrack(board)

        if (result != False): return board
        board[variable.pos] = 0 # remove {var = value from assignment}

    return False


def select_unassigned_variables(board):
    unassigned_variables = []

    for item in board.items():
        if (item[1] == 0):  # item[1] is the value of the variable
            variable = Var(item[0])
            variable.legal_val = find_legal_value(variable, board)
            unassigned_variables.append(variable)

    MRV_variable = min(unassigned_variables)
    return MRV_variable


def find_legal_value(variable, board):
    var_row = str(variable.pos[0])  # 'A'
    var_col = str(variable.pos[1])  # '2'
    var_box = get_box_num(variable)  # '1' , '2' , ... , '9'

    # check row
    for i in range(1, 10):  # i from 1 to 9
        if board[var_row + str(i)] != 0:
            variable.legal_val.discard(board[var_row + str(i)])

    # check column
    for r in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
        if board[r + var_col] != 0:
            variable.legal_val.discard(board[r + var_col])

    # check box
    if var_box == 1:
        variable.legal_val.discard(board['A1'])
        variable.legal_val.discard(board['A2'])
        variable.legal_val.discard(board['A3'])
        variable.legal_val.discard(board['B1'])
        variable.legal_val.discard(board['B2'])
        variable.legal_val.discard(board['B3'])
        variable.legal_val.discard(board['C1'])
        variable.legal_val.discard(board['C2'])
        variable.legal_val.discard(board['C3'])
    elif var_box == 2:
        variable.legal_val.discard(board['A4'])
        variable.legal_val.discard(board['A5'])
        variable.legal_val.discard(board['A6'])
        variable.legal_val.discard(board['B4'])
        variable.legal_val.discard(board['B5'])
        variable.legal_val.discard(board['B6'])
        variable.legal_val.discard(board['C4'])
        variable.legal_val.discard(board['C5'])
        variable.legal_val.discard(board['C6'])
    elif var_box == 3:
        variable.legal_val.discard(board['A7'])
        variable.legal_val.discard(board['A8'])
        variable.legal_val.discard(board['A9'])
        variable.legal_val.discard(board['B7'])
        variable.legal_val.discard(board['B8'])
        variable.legal_val.discard(board['B9'])
        variable.legal_val.discard(board['C7'])
        variable.legal_val.discard(board['C8'])
        variable.legal_val.discard(board['C9'])
    elif var_box == 4:
        variable.legal_val.discard(board['D1'])
        variable.legal_val.discard(board['D2'])
        variable.legal_val.discard(board['D3'])
        variable.legal_val.discard(board['E1'])
        variable.legal_val.discard(board['E2'])
        variable.legal_val.discard(board['E3'])
        variable.legal_val.discard(board['F1'])
        variable.legal_val.discard(board['F2'])
        variable.legal_val.discard(board['F3'])
    elif var_box == 5:
        variable.legal_val.discard(board['D4'])
        variable.legal_val.discard(board['D5'])
        variable.legal_val.discard(board['D6'])
        variable.legal_val.discard(board['E4'])
        variable.legal_val.discard(board['E5'])
        variable.legal_val.discard(board['E6'])
        variable.legal_val.discard(board['F4'])
        variable.legal_val.discard(board['F5'])
        variable.legal_val.discard(board['F6'])
    elif var_box == 6:
        variable.legal_val.discard(board['D7'])
        variable.legal_val.discard(board['D8'])
        variable.legal_val.discard(board['D9'])
        variable.legal_val.discard(board['E7'])
        variable.legal_val.discard(board['E8'])
        variable.legal_val.discard(board['E9'])
        variable.legal_val.discard(board['F7'])
        variable.legal_val.discard(board['F8'])
        variable.legal_val.discard(board['F9'])
    elif var_box == 7:
        variable.legal_val.discard(board['G1'])
        variable.legal_val.discard(board['G2'])
        variable.legal_val.discard(board['G3'])
        variable.legal_val.discard(board['H1'])
        variable.legal_val.discard(board['H2'])
        variable.legal_val.discard(board['H3'])
        variable.legal_val.discard(board['I1'])
        variable.legal_val.discard(board['I2'])
        variable.legal_val.discard(board['I3'])
    elif var_box == 8:
        variable.legal_val.discard(board['G4'])
        variable.legal_val.discard(board['G5'])
        variable.legal_val.discard(board['G6'])
        variable.legal_val.discard(board['H4'])
        variable.legal_val.discard(board['H5'])
        variable.legal_val.discard(board['H6'])
        variable.legal_val.discard(board['I4'])
        variable.legal_val.discard(board['I5'])
        variable.legal_val.discard(board['I6'])
    elif var_box == 9:
        variable.legal_val.discard(board['G7'])
        variable.legal_val.discard(board['G8'])
        variable.legal_val.discard(board['G9'])
        variable.legal_val.discard(board['H7'])
        variable.legal_val.discard(board['H8'])
        variable.legal_val.discard(board['H9'])
        variable.legal_val.discard(board['I7'])
        variable.legal_val.discard(board['I8'])
        variable.legal_val.discard(board['I9'])

    return variable.legal_val


def get_box_num(variable):
    possible_box = []
    row = variable.pos[0]  # item_in_board[0] is the key of the item
    col = int(variable.pos[1])

    if ((row == 'A') or (row == 'B') or (row == 'C')):
        possible_box = [1, 2, 3]
    elif ((row == 'D') or (row == 'E') or (row == 'F')):
        possible_box = [4, 5, 6]
    elif ((row == 'G') or (row == 'H') or (row == 'I')):
        possible_box = [7, 8, 9]

    if (col <= 3):
        possible_box = possible_box[0]
    elif ((col >= 4) and (col <= 6)):
        possible_box = possible_box[1]
    elif ((col >= 7)):
        possible_box = possible_box[2]

    return possible_box


if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
        end_time = time.time()
        time_used = end_time - start_time
        print('Time used = ', time_used)

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        end_time = time.time()
        time_used = end_time - start_time
        print('Time used = ', time_used)
        print("Finishing all boards in file.")
