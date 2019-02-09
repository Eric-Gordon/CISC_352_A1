import random
import time
import math
# import time to show speed of algorithm


def vertical_conflict(board, col):
    return (any(point == col for point in board))


def place_queens(size):
    #start = time.time()
    board = []
    for row in range(2):
        for col in range(row, size, 2):
            board.append(col)
    #print("{} placed_after: {:.10f}".format(size, time.time() - start))
    nd = get_negative_diagonals(board)
    # initial positive diagonal
    pd = get_positive_diagonals(board)
    # initial collision computation
    cols = compute_collisions(nd, pd)
    # initial attack computation
    attack = compute_attacks(nd, pd)
    noa = len(attack)
    return [board, nd, pd, cols, attack, noa]


def get_negative_diagonals(play_board, specific_difference=False):
    #start = time.time()
    total = []
    board = play_board[:]
    if specific_difference is False:
        for difference in range((len(board)-2), (((len(board)-1)) * -1), -1):
            queens = 0
            for row in range(len(board)):
                if (row - board[row]) == difference:
                    queens += 1
            total.append(queens)
        #print("negative_after: {:.10f}".format(time.time() - start))
        return total
    else:
        for row in range(len(board)):
            queens = 0
            if (row - board[row]) == specific_difference:
                queens += 1
        total.append(queens)
        return total


def get_positive_diagonals(play_board, specific_sum=False):
    #start = time.time()
    total = []
    board = play_board[:]
    if specific_sum is False:
        for summation in range(1, (((len(board))-1)+((len(board)-1)))):
            queens = 0
            for row in range(len(board)):
                if (row + board[row]) == summation:
                    queens += 1
            total.append(queens)
        #print("positive_after: {:.10f}".format(time.time() - start))
        return total
    else:
        for row in range(len(board)):
            queens = 0
            if (row + board[row]) == specific_sum:
                queens += 1
        total.append(queens)
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
    for row in range(len(negative_diagonals)):
        if negative_diagonals[row] > 0 and (row not in array):
            array.append(row)
    for row in range(len(positive_diagonals)):
        if positive_diagonals[row] > 0 and (row not in array):
            array.append(row)
    return array


def swap_ok(i, j, play_board):
    board = play_board[:]
    # setup old differences and sums
    i_old_difference = i - board[i]
    i_old_sum = i + board[i]
    j_old_difference = j - board[j]
    j_old_sum = j + board[j]
    # total the collisions
    i_old_negatives = get_negative_diagonals(board, i_old_difference)
    i_old_positives = get_positive_diagonals(board, i_old_sum)
    i_old_collisions = compute_collisions(i_old_negatives, i_old_positives)

    j_old_negatives = get_negative_diagonals(board, j_old_difference)
    j_old_positives = get_positive_diagonals(board, j_old_sum)
    j_old_collisions = compute_collisions(j_old_negatives, j_old_positives)
    print("j_negatives: {} -- j_positives: {} -- j_collisions: {}".format(
        j_old_negatives, j_old_positives, j_old_collisions))
    total_old = (compute_collisions(get_negative_diagonals(
        board, j_old_difference), get_positive_diagonals(board, j_old_sum)))

    # swap!
    board[i], board[j] = board[j], board[i]

    # setup new differences and sums
    i_new_difference = i - board[i]
    i_new_sum = i + board[i]
    j_new_difference = j - board[j]
    j_new_sum = j + board[j]
    # total the collisions
    total_new = (compute_collisions(get_negative_diagonals(board, i_new_difference), get_positive_diagonals(board, i_new_sum))) + \
        (compute_collisions(get_negative_diagonals(board, j_new_difference),
                            get_positive_diagonals(board, j_new_sum)))
    print("TOTAL_NEW: {} -- TOTAL_OLD: {}".format(total_new, total_old))
    if total_new < total_old:
        return True
    else:
        return False


def perform_swap(i, j, play_board):
    board = play_board[:]
    board[i], board[j] = board[j], board[i]
    start_negative_diagonals = time.time()
    nd = get_negative_diagonals(board)
    print("negative: {:.10f}".format(time.time() - start_negative_diagonals))
    start_positive_diagonals = time.time()
    pd = get_positive_diagonals(board)
    print("positive: {:.10f}".format(time.time() - start_positive_diagonals))
    cols = compute_collisions(nd, pd)
    return [board, nd, pd, cols]


def solve(size):
    collisions = -1
    c1 = 0.5
    c2 = 50
    while collisions != 0:
        place = place_queens(size)
        # initial board
        board = place[0]
        # initial negative diagonal
        negative_diagonals = place[1]
        # initial positive diagonal
        positive_diagonals = place[2]
        # initial collision computation
        collisions = place[3]
        # initial attack computation
        attack = place[4]
        # initial number of attacks
        number_of_attacks = place[5]

        limit = c1 * collisions

        loop = 0
        swaps = 0
        while loop < (c2 * size):
            print(
                "loop: {} -- swaps: {} -- collisions: {}".format(loop, swaps, collisions))
            k = 0
            while k < number_of_attacks:
                i = attack[k]
                j = random.randint(0, size-1)
                if swap_ok(i, j, board):
                    swap = perform_swap(i, j, board)
                    board = swap[0]
                    negative_diagonals = swap[1]
                    positive_diagonals = swap[2]
                    collisions = swap[3]
                    if collisions == 0:
                        break
                    if collisions < limit:
                        limit = c1 * collisions
                        attack = compute_attacks(
                            negative_diagonals[1], positive_diagonals[1])
                        number_of_attacks = len(attack)
                k += 1
            loop += loop + k
    return board


solutions = []
queens_file = open("nqueens.txt")
for n in queens_file:
    start = time.time()
    solution = solve(int(n))
    solutions.append(solution)
    print("n = {} -- Solution Found in: {}\n{}".format(n, time.time()-start, solution))
    print("******")
    print()
queens_file.close()

solution_file = open("nqueens_out.txt", "w")
for solution in solutions:
    solution_file.write("[ ")
    solution_file.write(' '.join(str(e) for e in solution))
    solution_file.write(" ]\n")
solution_file.close()
