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


def count_negative_diagonals(board):
    total = 0
    for difference in range((len(board)-1), (((len(board)-1)) * -1), -1):
        total += len(list(filter(lambda row: ((row -
                                               board[row]) == difference), board)))
    return total


def count_positive_diagonals(board):
    total = 0
    for sum in range(1, (((len(board))-1)+((len(board)-1)))):
        total += len(list(filter(lambda row: ((row +
                                               board[row]) == sum), board)))
    return total


def swap_ok(i, j, board):
    i_old_difference = i - board[i]
    i_old_sum = i + board[i]
    j_old_difference = j - board[j]
    j_old_sum = j + board[j]
    total_old = 0
    total_old += len(list(filter(lambda x: ((x +
                                             board[x]) == i_old_sum), board)))
    total_old += len(list(filter(lambda x: ((x +
                                             board[x]) == j_old_sum), board)))
    total_old += len(list(filter(lambda x: ((x -
                                             board[x]) == i_old_difference), board)))
    total_old += len(list(filter(lambda x: ((x -
                                             board[x]) == j_old_difference), board)))

    temp = board[i]
    board[i] = board[j]
    board[j] = temp
    i_new_difference = i - board[i]
    i_new_sum = i + board[i]
    j_new_difference = j - board[j]
    j_new_sum = j + board[j]
    total_new = 0
    total_new += len(list(filter(lambda x: ((x +
                                             board[x]) == i_new_sum), board)))
    total_new += len(list(filter(lambda x: ((x +
                                             board[x]) == j_new_sum), board)))
    total_new += len(list(filter(lambda x: ((x -
                                             board[x]) == i_new_difference), board)))
    total_new += len(list(filter(lambda x: ((x -
                                             board[x]) == j_new_difference), board)))

    print("TOTAL OLD = {} --- TOTAL NEW = {}".format(total_old, total_new))
    if total_new < total_old:
        return True
    else:
        return False


def perform_swap(i, j, board):
    temp = board[i]
    board[i] = board[j]
    board[j] = temp
    return board


def get_attacks(negative_diagonals, positive_diagonals):
    merged = []
    for queen in negative_diagonals:
        if queen not in merged:
            merged.append(queen)
    for queen in positive_diagonals:
        if queen not in merged:
            merged.append(queen)
    return merged


def solve(size):
    board = place_queens(size)
    negative_diagonals = count_negative_diagonals(board)
    positive_diagonals = count_positive_diagonals(board)
    collisions = negative_diagonals + positive_diagonals
    attack = get_attacks(negative_diagonals, positive_diagonals)
    number_of_attacks = len(attack)
    limit = 0.5 * collisions

    loop = 0
    while loop < (32 * size):
        for k in range(number_of_attacks):
            i = attack[k]
            j = random.randint(0, size-1)
            if swap_ok(i, j, board):
                board = perform_swap(i, j, board)
                negative_diagonals = count_negative_diagonals(board)
                positive_diagonals = count_positive_diagonals(board)
                collisions = (len(negative_diagonals) - 1) + \
                    (len(positive_diagonals) - 1)
                if collisions == 0:
                    break
                if collisions < limit:
                    limit = 0.5 * collisions
                    attack = get_attacks(
                        negative_diagonals, positive_diagonals)
                    number_of_attacks = len(attack)
            loop += loop + number_of_attacks
    if collisions != 0:
        print_solution(board, size)
        solve(size)
    else:
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
