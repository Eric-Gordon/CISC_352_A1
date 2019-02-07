import random
import time
import math
# import time to show speed of algorithm

# this will need to be converted to a file reader
# the assignment describes a text file with different n sizes


def take_input():
    """Accepts the size of the chess board"""
    while True:
        try:
            size = int(input('What is the size of the chessboard? n = \n'))
            if size == 1:
                print("Trivial solution, choose a board size of at least 4")
            if size <= 3:
                print("Enter a value such that size>=4")
                continue
            return size
        except ValueError:
            print("Invalid value entered. Enter again")

# this creates an n x n board with 0's


def get_board(size):
    """Returns an n by n board"""
    board = [0]*size
    for ix in range(size):
        board[ix] = [0]*size
    return board

# helper function for randomly placing queens on a safe row
# this makes sure the row doesn't contain another queen


def safe_horizontal(board, row, col, size):
    if(1 in board[row]):
        return False
    else:
        return True

# this functions loops through all of the columns of the board
# and places a queen on a random row, it checks that the row
# doesn't already contain a queen


def place_queens(board, size):
    for col in range(size):
        new_queen = random.randint(0, size-1)
        while not (safe_horizontal(board, new_queen, col, size)):
            new_queen = random.randint(0, size-1)
        board[new_queen][col] = 1

    return board

# counts conflicts to the left of the point given


def left_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + left_of(board, row, col-1, size)
        else:
            return left_of(board, row, col-1, size)

# counts conflicts to the right of the point given


def right_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + right_of(board, row, col+1, size)
        else:
            return right_of(board, row, col+1, size)


def right_diagonal_up_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + right_diagonal_up_of(board, row-1, col+1, size)
        else:
            return right_diagonal_up_of(board, row-1, col+1, size)


def right_diagonal_down_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + right_diagonal_down_of(board, row+1, col+1, size)
        else:
            return right_diagonal_down_of(board, row+1, col+1, size)


def left_diagonal_up_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + left_diagonal_up_of(board, row-1, col-1, size)
        else:
            return left_diagonal_up_of(board, row-1, col-1, size)


def left_diagonal_down_of(board, row, col, size):
    if row < 0 or row >= size or col < 0 or col >= size:
        return 0
    else:
        if board[row][col] == 1:
            return 1 + left_diagonal_down_of(board, row+1, col-1, size)
        else:
            return left_diagonal_down_of(board, row+1, col-1, size)

# main function to calculate all of the conflicts for a particular point


def conflicts(board, row, col, size):
    """Check if it's safe to place a queen at board[x][y]"""
    if(row < 0 or row >= size or col < 0 or col >= size):
        return 0
    else:
        return left_of(board, row, col-1, size) + right_of(board, row, col+1, size) + right_diagonal_up_of(board, row-1, col+1, size) + right_diagonal_down_of(board, row+1, col+1, size) + left_diagonal_up_of(board, row-1, col-1, size) + left_diagonal_down_of(board, row+1, col-1, size)


def min_conflict(board, col, size):
    conflict_array = []
    min_val, min_row, min_col = 10000, 0, col
    max_val, max_row = 0, 0
    current_row = 0
    for row in range(size):
        conflict_num = conflicts(board, row, col, size)
        conflict_array.append(conflict_num)
        if conflict_num < min_val:
            min_val = conflict_num
            min_row = row
        if conflict_num > max_val:
            max_val = conflict_num
            max_row = row
        if board[row][col] == 1:
            current_row = row
    return [min_row, min_col, current_row, min_val, max_row]


def check_solution(board, size):
    solution = True
    row = 0
    while solution and row < size-1:
        if 1 not in board[row]:
            solution = False
        else:
            if(conflicts(board, row, board[row].index(1), size) != 0):
                solution = False
        row += 1
    return solution


# somewhat of a solver function, this will need some work


def solve(board, max_steps, size):
    solution = False
    col = random.randint(0, size-1)
    steps = 0
    while not solution and steps < max_steps:
        min_row = min_conflict(board, col, size)
        if(min_row[0] != min_row[2]):
            if 1 in board[min_row[0]]:
                col = board[min_row[0]].index(1)
            else:
                col = random.randint(0, size-1)
            board[min_row[0]][min_row[1]] = 1
            board[min_row[2]][min_row[1]] = 0
            if min_row[3] == 0:
                solution = check_solution(board, size)
        steps += 1
    return [solution, board]


# this currently prints the board visually to see all of the queens
# the commented section in this function will print the 1D array
# of the column location for each queen in a row


def print_solution(board, size):
    # for row in board:
    #     print(row)
    # print()
    print("[", end=" ")
    for row in range(size-1):
        print(board[row].index(1), end=" ")
    print(board[size-1].index(1), end=" ]\n")


# take user input for n queens
size = take_input()
# generate the board
board = [x[:] for x in [[0] * size] * size]

# place all of the queens on the board
random_board = place_queens(board, size)

start_time = time.time()
solution = False
while not solution:
    solution = check_solution(random_board, size)

    solution_board = solve(random_board, 12, size)

    solution = solution_board[0]

    # generate the board
    board = [x[:] for x in [[0] * size] * size]

    # place all of the queens on the board
    random_board = place_queens(board, size)

print("SOLUTION FOUND IN {}".format(time.time()-start_time))
# print the board
print_solution(solution_board[1], size)
