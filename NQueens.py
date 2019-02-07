import random

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

# counts conflicts to the left of the point given


def count_left(board, row, col, size):
    conflicts = 0
    while col > 0:
        if board[row][col] == 1:
            conflicts += 1
        col -= 1
    return conflicts

# counts conflicts to the right of the point given


def count_right(board, row, col, size):
    conflicts = 0
    while col < size:
        if board[row][col] == 1:
            conflicts += 1
        col += 1
    return conflicts

# main function to calculate all of the conflicts for a particular point


def conflicts(board, row, col, size):
    """Check if it's safe to place a queen at board[x][y]"""
    if(row == size or col == size):
        return 0
    else:
        if(row == 0):
            if(col > 0 and col < size):
                return 0

    # # check diagonal up and to the left of row,col
    # up_left_x, up_left_y = row-1, col-1
    # while up_left_x > 0 and up_left_y > 0:
    #     if board[up_left_x][up_left_y] == 1:
    #         conflicts += 1
    #     up_left_x -= 1
    #     up_left_y -= 1

    # check diagonal up and to the right of row,col
    if(row-1 > 0 and col+1 < size):
        up_right_x, up_right_y = row-1, col+1
        while up_right_x < 0 and up_right_y < size:
            if board[up_right_x][up_right_y] == 1:
                conflicts += 1
            up_right_x += 1
            up_right_y += 1

    # # check diagonal down and to the left of row,col
    # down_left_x, down_left_y = row+1, col-1
    # while down_left_x > 0 and down_left_y >= 0:
    #     if board[down_left_x][down_left_y] == 1:
    #         conflicts += 1
    #     up_left_x -= 1
    #     up_left_y -= 1

    # check diagonal down and to the right of row,col
    if(row+1 < size and col+1 < size):
        down_right_x, down_right_y = row+1, col+1
        while down_right_x < size and down_right_y < size:
            if board[down_right_x][down_right_y] == 1:
                conflicts += 1
            down_right_x += 1
            down_right_y += 1

    return conflicts

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

# somewhat of a solver function, this will need some work


def solve(board, size):
    for row in range(size):
        print(conflicts(board, row, 0, size))

# this currently prints the board visually to see all of the queens
# the commented section in this function will print the 1D array
# of the column location for each queen in a row


def print_solution(board, size):
    for row in board:
        print(row)
    # print("[", end=" ")
    # for row in range(size-1):
    #     print(board[row].index(1), end=" ")
    # print(board[size-1].index(1), end=" ]\n")


# take user input for n queens
size = take_input()

# generate the board
board = get_board(size)

# place all of the queens on the board
random_board = place_queens(board, size)

# print the board
print_solution(random_board, size)

# solve(random_board, size)
