import random
import time
import math
# import time to show speed of algorithm


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


def get_negative_diagonals(play_board, specific_difference=False):
    total, array = [], []
    board = play_board[:]
    if specific_difference is False:
        for difference in range((len(board)-1), (((len(board)-1)) * -1), -1):
            queens = list(
                filter(lambda row: ((row - board[row]) == difference), board))
            if len(queens) > 1:
                for row in queens:
                    if row not in array:
                        array.append(row)
            total.append(len(queens))
        return [total, array]
    else:
        queens = list(
            filter(lambda row: ((row - board[row]) == specific_difference), board))
        total.append(len(queens))
        return total


def get_positive_diagonals(play_board, specific_sum=False):
    total, array = [], []
    board = play_board[:]
    if specific_sum is False:
        for summation in range(1, (((len(board))-1)+((len(board)-1)))):
            queens = list(
                filter(lambda row: ((row + board[row]) == summation), board))
            if len(queens) > 1:
                for row in queens:
                    if row not in array:
                        array.append(row)
            total.append(len(queens))
        return [total, array]
    else:
        queens = list(
            filter(lambda row: ((row + board[row]) == specific_sum), board))
        total.append(len(queens))
        return total


def compute_collisions(nd, pd):
    total = 0
    negative_diagonals, positive_diagonals = nd[:], pd[:]
    for diagonal in negative_diagonals:
        if diagonal > 1:
            total += diagonal - 1
    for diagonal in positive_diagonals:
        if diagonal > 1:
            total += diagonal - 1
    return total


def compute_attacks(nd, pd):
    array = []
    negative_diagonals, positive_diagonals = nd[:], pd[:]
    for row in negative_diagonals:
        if row not in array:
            array.append(row)
    for row in positive_diagonals:
        if row not in array:
            array.append(row)
    return array


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
    collisions = -1
    c1 = 0.45
    c2 = 32
    while collisions != 0:
        board = place_queens(size)
        negative_diagonals = get_negative_diagonals(board)
        positive_diagonals = get_positive_diagonals(board)
        collisions = compute_collisions(
            negative_diagonals[0], positive_diagonals[0])
        attack = compute_attacks(negative_diagonals[1], positive_diagonals[1])

        number_of_attacks = len(attack)
        limit = c1 * collisions

        loop = 0
        while loop < (c2 * size):
            k = 0
            while k < number_of_attacks:
                i = attack[k]
                j = random.randint(0, size-1)
                if swap_ok(i, j, board):
                    board = perform_swap(i, j, board)
                    negative_diagonals = get_negative_diagonals(board)
                    positive_diagonals = get_positive_diagonals(board)
                    collisions = compute_collisions(
                        negative_diagonals[0], positive_diagonals[0])
                    if collisions == 0:
                        break
                    if collisions < limit:
                        limit = c1 * collisions
                        attack = compute_attacks(
                            negative_diagonals[1], positive_diagonals[1])
                        number_of_attacks = len(attack)
                k += 1
            loop += loop + number_of_attacks
    return board


solutions = []
queens_file = open("nqueens.txt")
for n in queens_file:
    start = time.time()
    print("n = {}".format(int(n)))
    solution = solve(int(n))
    solutions.append(solution)
    print("Solution Found in: {}\n{}".format(time.time()-start, solution))
    print("******")
    print()
queens_file.close()

solution_file = open("nqueens_out.txt", "w")
for solution in solutions:
    solution_file.write("{}\n".format(solution))
solution_file.close()
