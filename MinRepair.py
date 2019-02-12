import random
import time
import math
# import time to show speed of algorithm


def place_queens(size):
    # start = time.time()
    taken_negatives = []
    board = []
    for i in range(2):
        for col in range(i, size, 2):
            board.append(col)
    # for row in range(len(board), size):
    #     col = random.choice(
    #         list(free_col for free_col in range(size) if free_col not in board))
    #     board.append(col)
    # board = list(random.sample(range(size), size))
    # print("board created in: {:.10f}".format(time.time() - start))
    return board


def get_diagonals(play_board, nds, pds):
    nd, pd, p_d_rows, n_d_rows = {}, {}, {}, {}
    # start = time.time()
    for row in range(len(play_board)):
        if(row - play_board[row]) in nds:
            if (row - play_board[row]) not in n_d_rows:
                n_d_rows[(row - play_board[row])] = [row]
            else:
                n_d_rows[(row - play_board[row])].append(row)
            if (row - play_board[row]) not in nd:
                nd[(row - play_board[row])] = 1
            else:
                nd[(row - play_board[row])] += 1
        if(row + play_board[row]) in pds:
            if (row + play_board[row]) not in p_d_rows:
                p_d_rows[(row + play_board[row])] = [row]
            else:
                p_d_rows[(row + play_board[row])].append(row)
            if (row + play_board[row]) not in pd:
                pd[(row + play_board[row])] = 1
            else:
                pd[(row + play_board[row])] += 1
    # print("diagonals calculated in: {:.10f}".format(time.time() - start))
    return [nd, pd, n_d_rows, p_d_rows]


def compute_collisions(nd, pd, n_rows, p_rows):
    total = 0
    under_attack = []
    # start = time.time()
    for diagonal in nd:
        if nd[diagonal] > 1:
            total += (nd[diagonal] - 1)
            for row in n_rows[diagonal]:
                if row not in under_attack:
                    under_attack.append(row)
    for diagonal in pd:
        if pd[diagonal] > 1:
            total += (pd[diagonal] - 1)
            for row in p_rows[diagonal]:
                if row not in under_attack:
                    under_attack.append(row)
    # print("collisions totaled in: {:.10f}".format(time.time() - start))
    return [total, under_attack]


def get_specific_negative_diagonal(play_board, diff):
    total = 0
    for row in range(len(play_board)):
        if (row - play_board[row]) == diff:
            total += 1
    return (total - 1) if (total > 1) else 0


def get_specific_positive_diagonal(play_board, summ):
    total = 0
    for row in range(len(play_board)):
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
    diagonals = get_diagonals(board, nds, pds)
    under_attack_rows = compute_collisions(
        diagonals[0], diagonals[1], diagonals[2], diagonals[3])
    return [board, under_attack_rows]


def compute_min_repair(play_board, row):
    cols = []
    for col in range(len(play_board)):
        col_old = get_specific_negative_diagonal(play_board, (row - col)) + get_specific_positive_diagonal(
            play_board, (row + col)) + (1 if col in play_board else 0)
        cols.append(col_old)
    min_col = random.choice(list(conflict for conflict in range(
        len(cols)) if cols[conflict] == min(cols)))
    return min_col


def solve(size):
    collisions = -1
    difference = list(range((size-2), ((size-1) * -1), -1))
    summation = list(range(1, ((size-1)+(size-1))))
    c1 = 0.45
    c2 = 32

    while collisions != 0:
        board = place_queens(size)
        diagonals = get_diagonals(board, difference, summation)
        under_attack_rows = compute_collisions(
            diagonals[0], diagonals[1], diagonals[2], diagonals[3])
        collisions = under_attack_rows[0]
        attack = under_attack_rows[1]
        number_of_attacks = len(attack)

        limit = c1 * collisions

        loop = 0
        while loop < (c2 * size) and collisions != 0:
            print("loop: {}\ncollisions: {}\nnoa: {}".format(
                loop, collisions, number_of_attacks))
            k = 0
            while k < number_of_attacks and collisions != 0:
                print("loop: {}\ncollisions: {}\nk: {}".format(
                    loop, collisions, k))
                i = attack[k]
                # potentially make j use min conflict on row i
                j = board.index(compute_min_repair(board, i))
                # j = random.randint(0, size-1)
                if swap_ok(i, j, board):
                    swap = perform_swap(i, j, difference, summation, board)
                    board = swap[0]
                    collisions = swap[1][0]
                    attack = swap[1][1]
                    number_of_attacks = len(attack)
                    if collisions == 0:
                        break
                    if collisions < limit:
                        limit = c1 * collisions

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
    print("Solution Found in: {}\n".format(time.time()-start))
    print("******")
    print()
queens_file.close()

solution_file = open("nqueens_out.txt", "w")
for solution in solutions:
    solution_file.write("{}\n".format(solution))
solution_file.close()
