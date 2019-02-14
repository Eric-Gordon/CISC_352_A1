import random
import time
import math
# import time to show speed of algorithm


def place_queens(size):
    # max collisions allowed on generation
    c_range = 50
    # initialize
    global taken_negatives, taken_positives
    taken_negatives = {}
    taken_positives = {}
    free_cols = list(range(size))
    board = []

    board_len = 0
    while (board_len < (size - c_range)):
        board_len = len(board)
        col = random.choice(free_cols)
        if (board_len + col) not in taken_positives and (board_len - col) not in taken_negatives:
            taken_negatives[(board_len - col)] = [board_len]
            taken_positives[(board_len + col)] = [board_len]
            free_cols.remove(col)
            board.append(col)
    for row in range(len(board), size):
        col = random.choice(free_cols)
        free_cols.remove(col)
        board.append(col)
    return board


def get_diagonals(play_board, nds, pds):
    nd, pd = {}, {}
    for row in range(0, len(play_board)):
        if(row - play_board[row]) in nds:
            if (row - play_board[row]) not in taken_negatives:
                taken_negatives[(row - play_board[row])] = [row]
            else:
                taken_negatives[(row - play_board[row])].append(row)
            if (row - play_board[row]) not in nd:
                nd[(row - play_board[row])] = 1
            else:
                nd[(row - play_board[row])] += 1
        if(row + play_board[row]) in pds:
            if (row + play_board[row]) not in taken_positives:
                taken_positives[(row + play_board[row])] = [row]
            else:
                taken_positives[(row + play_board[row])].append(row)
            if (row + play_board[row]) not in pd:
                pd[(row + play_board[row])] = 1
            else:
                pd[(row + play_board[row])] += 1
    return [{k: v for k, v in nd.items() if v > 1}, {k: v for k, v in pd.items() if v > 1}]


def compute_collisions(nd, pd):
    total = 0
    for diagonal in nd:
        total += (nd[diagonal] - 1)

    for diagonal in pd:
        total += (pd[diagonal] - 1)
    return total


def compute_attacks(nd, pd):
    under_attack = []
    for diagonal in nd:
        for row in taken_negatives[diagonal]:
            if row not in under_attack:
                under_attack.append(row)
    for diagonal in pd:
        for row in taken_positives[diagonal]:
            if row not in under_attack:
                under_attack.append(row)
    return under_attack


def get_specific_negative_diagonal(play_board, diff):
    total = 0
    for row in range(0, len(play_board)):
        if (row - play_board[row]) == diff:
            total += 1
    return (total - 1) if (total > 1) else 0


def get_specific_positive_diagonal(play_board, summ):
    total = 0
    for row in range(0, len(play_board)):
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


def perform_swap(i, j, nds, pds, play_board):
    board = play_board[:]
    board[i], board[j] = board[j], board[i]
    taken_negatives, taken_positives = {}, {}
    diagonals = get_diagonals(board, nds, pds)
    return [board, diagonals]


def solve(size):
    collisions = -1
    global difference, summation
    difference = list(range((size-2), ((size-1) * -1), -1))
    summation = list(range(1, ((size-1)+(size-1))))
    c1 = 0.6
    c2 = 32

    while collisions != 0:
        board = place_queens(size)
        diagonals = get_diagonals(board, difference, summation)
        collisions = compute_collisions(diagonals[0], diagonals[1])
        attack = compute_attacks(diagonals[0], diagonals[1])
        number_of_attacks = len(attack)

        limit = c1 * collisions

        loop = 0
        while loop < (c2 * size) and collisions != 0:
            # print("MAIN: loop: {} -- collisions: {} -- noa: {}".format(loop,collisions, number_of_attacks))
            k = 0
            while k < number_of_attacks and collisions != 0:
                i = attack[k]
                # potentially make j use min conflict on row i
                # j = board.index(compute_min_repair(board, i))
                # j = random.choice(attack) if len(attack) > (size / 10) else random.randint(0, size-1)
                j = random.randint(0, size-1)
                # print("collisions: {}\ni: {}\nj: {}".format(collisions, i, j))
                if swap_ok(i, j, board):
                    swap = perform_swap(i, j, difference, summation, board)
                    board = swap[0]
                    collisions = compute_collisions(swap[1][0], swap[1][1])
                    if collisions == 0:
                        break
                    if collisions < limit:
                        limit = c1 * collisions
                        attack = compute_attacks(swap[1][0], swap[1][1])
                        number_of_attacks = len(attack)

                k += 1
            loop += number_of_attacks
    return board


solutions = []
queens_file = open("nqueens.txt")
for n in queens_file:
    start = time.time()
    print("n = {}".format(int(n)))
    solution = solve(int(n))
    solutions.append(solution)
    print("Solution Found in: {:.10f}\n".format(time.time()-start))
    print("******")
    print()
queens_file.close()

solution_file = open("nqueens_out.txt", "w")
for solution in solutions:
    solution_file.write("{}\n".format(solution))
solution_file.close()
