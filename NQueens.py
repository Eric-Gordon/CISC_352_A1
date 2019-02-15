import random
import time
import math
# import time to show speed of algorithm


def place_queens(size):
    # max collisions allowed on generation
    c_range = 0
    if size > 1000000:
        c_range = 100
    elif size > 100000:
        c_range = 80
    elif size > 10000:
        c_range = 50
    elif size > 1000:
        c_range = 40
    else:
        c_range = 30

    # initialize
    taken_negatives = {}
    taken_positives = {}
    free_cols = list(range(size))
    board = []

    board_len = 0
    while (board_len < (size - c_range)):
        board_len = len(board)
        col = random.choice(free_cols)
        if (board_len + col) not in taken_positives and (board_len - col) not in taken_negatives:
            if (board_len - col) in difference:
                taken_negatives[(board_len - col)] = [board_len]
            if (board_len + col) in summation:
                taken_positives[(board_len + col)] = [board_len]
            free_cols.remove(col)
            board.append(col)
    for row in range(len(board), size):
        col = random.choice(free_cols)
        free_cols.remove(col)
        board.append(col)
    return board


def compute_collisions(board):
    total, nd, pd = 0, {}, {}
    for row in range(len(board)):
        diff = row - board[row]
        summ = row + board[row]
        if diff in difference:
            if diff in nd:
                nd[diff].append(row)
                total += 1
            else:
                nd[diff] = [row]
        if summ in summation:
            if summ in pd:
                pd[summ].append(row)
                total += 1
            else:
                pd[summ] = [row]
    return [total, nd, pd]


def compute_attacks(nd, pd):
    under_attack = []
    for diagonal in nd:
        if len(nd[diagonal]) > 1:
            for row in nd[diagonal]:
                if row not in under_attack:
                    under_attack.append(row)
    for diagonal in pd:
        if len(pd[diagonal]) > 1:
            for row in pd[diagonal]:
                if row not in under_attack:
                    under_attack.append(row)
    return under_attack


def get_specific_negative_diagonal(play_board, diff):
    total, n = 0, len(play_board)
    for row in range(0, n):
        if (row - play_board[row]) == diff:
            total += 1
    return (total - 1) if (total > 1) else 0


def get_specific_positive_diagonal(play_board, summ):
    total, n = 0, len(play_board)
    for row in range(0, n):
        if (row + play_board[row]) == summ:
            total += 1
    return (total - 1) if (total > 1) else 0


def swap_ok(i, j, play_board):
    if i == j:
        return False
    board = play_board[:]

    # setup old differences and sums
    i_old = get_specific_negative_diagonal(
        board, (i - board[i])) + get_specific_positive_diagonal(board, (i + board[i]))
    j_old = get_specific_negative_diagonal(
        board, (j - board[j])) + get_specific_positive_diagonal(board, (j + board[j]))
    total_old = i_old + j_old

    # swap!
    board[i], board[j] = board[j], board[i]

    i_new = get_specific_negative_diagonal(
        board, (i - board[i])) + get_specific_positive_diagonal(board, (i + board[i]))
    j_new = get_specific_negative_diagonal(
        board, (j - board[j])) + get_specific_positive_diagonal(board, (j + board[j]))
    total_new = i_new + j_new
    if total_new < total_old:
        return True
    else:
        return False


def solve(size):
    collisions = -1
    global difference, summation
    difference = list(range((size-2), ((size-1) * -1), -1))
    summation = list(range(1, ((size-1)+(size-1))))

    while collisions != 0:
        board = place_queens(size)
        compute = compute_collisions(board)
        collisions = compute[0]
        nd, pd = compute[1], compute[2]
        attack = compute_attacks(nd, pd)
        limit = 0.8 * collisions
        loop = 0
        while loop < (32 * size) and collisions != 0:
            # print("UPDATED: collisions: {}".format(collisions))
            k = 0
            while k < len(attack):
                i = attack[k]
                j = random.randint(0, size - 1)
                if swap_ok(i, j, board):
                    board[i], board[j] = board[j], board[i]
                    compute = compute_collisions(board)
                    collisions = compute[0]
                    nd, pd = compute[1], compute[2]
                    if collisions == 0:
                        break
                    if collisions < limit:
                        limit = 0.8 * collisions
                        attack = compute_attacks(nd, pd)
                k += 1
            loop += len(attack)
    return board


solutions = []
queens_file = open("nqueens.txt")
for n in queens_file:
    solution = solve(int(n))
    solutions.append(solution)
queens_file.close()

solution_file = open("nqueens_out.txt", "w")
for solution in solutions:
    solution_file.write("{}\n".format(solution))
solution_file.close()
