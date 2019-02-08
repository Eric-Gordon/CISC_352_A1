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


def vertical_conflict(board, col):
    return (any(point == col for point in board))


def place_queens(size):
    board = []
    for row in range(size):
        col = random.randint(0, size-1)
        while vertical_conflict(board, col):
            col = random.randint(0, size-1)
        board.append(col)
    return board


def get_negative_diagonals(board, specific_difference=False):
    total, attack = [], []
    if specific_difference is False:
        for difference in range((len(board)-1), (((len(board)-1)) * -1), -1):
            queens = list(
                filter(lambda row: ((row - board[row]) == difference), board))
            if len(queens) > 1:
                for row in queens:
                    if row not in attack:
                        attack.append(row)
            total.append(len(queens))
        return [total, attack]
    else:
        queens = list(
            filter(lambda row: ((row - board[row]) == specific_difference), board))
        total.append(len(queens))
        return total


def get_positive_diagonals(board, specific_sum=False):
    total, attack = [], []
    if specific_sum is False:
        for summation in range(1, (((len(board))-1)+((len(board)-1)))):
            queens = list(
                filter(lambda row: ((row + board[row]) == summation), board))
            if len(queens) > 1:
                for row in queens:
                    if row not in attack:
                        attack.append(row)
            total.append(len(queens))
        return [total, attack]
    else:
        queens = list(
            filter(lambda row: ((row + board[row]) == specific_sum), board))
        total.append(len(queens))
        return total


def compute_collisions(negative_diagonals, positive_diagonals):
    total = 0
    for diagonal in negative_diagonals:
        if diagonal > 1:
            total += diagonal - 1
    for diagonal in positive_diagonals:
        if diagonal > 1:
            total += diagonal - 1
    return total


def compute_attacks(negative_diagonals, positive_diagonals):
    attack = []
    for row in negative_diagonals:
        if row not in attack:
            attack.append(row)
    for row in positive_diagonals:
        if row not in attack:
            attack.append(row)
    return attack


def swap_ok(i, j, play_board):
    board = play_board[:]
    # setup old differences and sums
    i_old_difference = i - board[i]
    i_old_sum = i + board[i]
    j_old_difference = j - board[j]
    j_old_sum = j + board[j]
    # get old conflicts
    total_old = 0

    # old i diagonals
    i_old_negative_diagonal = get_negative_diagonals(board, i_old_difference)
    i_old_positive_diagonal = get_positive_diagonals(board, i_old_sum)
    # calculate i old collisions
    i_old_collisions = compute_collisions(
        i_old_negative_diagonal, i_old_positive_diagonal)

    # old j diagonals
    j_old_negative_diagonal = get_negative_diagonals(board, j_old_difference)
    j_old_positive_diagonal = get_positive_diagonals(board, j_old_sum)
    # calculate j old collisions
    j_old_collisions = compute_collisions(
        j_old_negative_diagonal, j_old_positive_diagonal)

    # total the collisions
    total_old += i_old_collisions + j_old_collisions

    # swap!
    board[i], board[j] = board[j], board[i]

    # setup new differences and sums
    i_new_difference = i - board[i]
    i_new_sum = i + board[i]
    j_new_difference = j - board[j]
    j_new_sum = j + board[j]
    # get new conflicts
    total_new = 0

    # new i diagonals
    i_new_negative_diagonal = get_negative_diagonals(board, i_new_difference)
    i_new_positive_diagonal = get_positive_diagonals(board, i_new_sum)
    # calculate i new collisions
    i_new_collisions = compute_collisions(
        i_new_negative_diagonal, i_new_positive_diagonal)

    # old j diagonals
    j_new_negative_diagonal = get_negative_diagonals(board, j_new_difference)
    j_new_positive_diagonal = get_positive_diagonals(board, j_new_sum)
    # calculate j old collisions
    j_new_collisions = compute_collisions(
        j_new_negative_diagonal, j_new_positive_diagonal)

    # total the collisions
    total_new += i_new_collisions + j_new_collisions
    if total_new < total_old:
        return True
    else:
        return False


def perform_swap(i, j, play_board):
    board = play_board[:]
    board[i], board[j] = board[j], board[i]
    return board


def solve(size):
    board = place_queens(size)
    negative_diagonals = get_negative_diagonals(board)
    positive_diagonals = get_positive_diagonals(board)
    collisions = compute_collisions(
        negative_diagonals[0], positive_diagonals[0])
    attack = compute_attacks(negative_diagonals[1], positive_diagonals[1])

    number_of_attacks = len(attack)
    limit = 0.5 * collisions

    loop = 0
    while loop < (32 * size):
        for k in range(number_of_attacks):
            i = attack[k]
            j = random.randint(0, size-1)
            if swap_ok(i, j, board):
                board = perform_swap(i, j, board)
                negative_diagonals = get_negative_diagonals(board)
                positive_diagonals = get_positive_diagonals(board)
                collisions = compute_collisions(
                    negative_diagonals[0], positive_diagonals[0])
                if collisions == 0:
                    loop += (50 * size)
                if collisions < limit:
                    limit = 0.5 * collisions
        loop += loop + number_of_attacks

    print("FINAL: collisions = {} -- number_of_attacks = {}".format(collisions, number_of_attacks))
    return board


# this currently prints the board visually to see all of the queens
# the commented section in this function will print the 1D array
# of the column location for each queen in a row


def print_solution(board, size):
    for row in board:
        print(row)
    print()
    # print("[", end=" ")
    # for row in range(size-1):
    #     print(board[row].index(1), end=" ")
    # print(board[size-1].index(1), end=" ]\n")


# take user input for n queens
size = take_input()
print("****")

solved = solve(size)

print_solution(solved, size)

# start_time = time.time()
# solution = False
# while not solution:
#     solution = check_solution(random_board, size)

#     solution_board = solve(random_board, 7, size)

#     solution = solution_board[0]

#     # generate the board
#     board = [x[:] for x in [[0] * size] * size]

#     # place all of the queens on the board
#     random_board = place_queens(board, size)

# print("SOLUTION FOUND IN {}".format(time.time()-start_time))
# # print the board
# print_solution(solution_board[1], size)
