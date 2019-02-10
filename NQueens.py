import random
import time
import math
# import time to show speed of algorithm


def vertical_conflict(board, col):
    return (any(point == col for point in board))


def place_queens(size):
    # for row in range(size):
    #     col = random.randint(0, size-1)
    #     while vertical_conflict(board, col):
    #         col = random.randint(0, size-1)
    #     board.append(col)
    # board = []
    # left_diagonal = []
    # right_diagonal = []
    # #start = time.time()
    # for row in range(math.floor(size/2)):
    #     col = random.choice(list(free_col for free_col in range(size) if (free_col not in board and (
    #         row - free_col) not in left_diagonal and (row + free_col) not in right_diagonal)))
    #     left_diagonal.append(row - col)
    #     right_diagonal.append(row + col)
    #     board.append(col)
    # for row in range(math.floor(size/2), size):
    #     col = random.choice(
    #         list(free_col for free_col in range(size) if free_col not in board))
    #     board.append(col)
    # #print("placement_time: {:.10f}".format(time.time() - start))
    # return board
    board = list(random.sample(range(size), size))
    return board


def get_negative_diagonals(play_board, specific_difference=False):
    total, array = [], []
    board = play_board[:]
    if specific_difference is False:
        for difference in range((len(board)-2), (((len(board)-1)) * -1), -1):
            queens = list(
                filter(lambda row: ((row - board[row]) == difference), board))
            if len(queens) > 1:
                for row in queens:
                    if row not in array:
                        array.append(row)
            total.append([difference, len(queens)])
        return [total, array]
    else:
        queens = list(
            filter(lambda row: ((row - board[row]) == specific_difference), board))
        total.append([specific_difference, len(queens)])
        return total


# def get_diagonals(play_board, specific_difference=False, specific_sum=False):
#     nd_temp, nd_total, pd_temp, pd_total = [], [], [], []
#     board = play_board[:]
#     if specific_difference is False and specific_sum is False:
#         difference = list(range((len(board)-2), (((len(board)-1)) * -1), -1))
#         summation = list(range(1, (((len(board))-1)+((len(board)-1)))))
#         for row in range(len(board)):
#             if(row - board[row]) in difference:
#                 nd_temp.append(row - board[row])
#             if(row+board[row]) in summation:
#                 pd_temp.append(row + board[row])

#         d_diffs = (list(set(nd_temp)))
#         d_sums = (list(set(pd_temp)))
#         for diff in d_diffs:
#             queens = nd_temp.count(diff)
#             nd_total.append([diff, queens])
#         for summ in d_sums:
#             queens = pd_temp.count(summ)
#             pd_total.append([summ, queens])
#         return [nd_total, pd_total]
#     else:
#         queens = list(
#             filter(lambda row: ((row - board[row]) == specific_difference), board))
#         total.append([specific_difference, len(queens)])
#         return total


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
            total.append([summation, len(queens)])
        return [total, array]
    else:
        queens = list(
            filter(lambda row: ((row + board[row]) == specific_sum), board))
        total.append([specific_sum, len(queens)])
        return total
# def get_positive_diagonals(play_board, specific_sum=False):
#     total = []
#     board = play_board[:]
#     if specific_sum is False:
#         summation = list(range(1, (((len(board))-1)+((len(board)-1)))))
#         for row in range(len(board)):
#             if (row + board[row]) in summation:
#                 total.append(summation)
#         new_total = []
#         for d_sum in total:
#             queens = total.count(d_sum)
#             new_total.append([d_sum, queens])
#         return new_total
#     else:
#         queens = list(
#             filter(lambda row: ((row + board[row]) == specific_sum), board))
#         total.append([specific_sum, len(queens)])
#         return total


def compute_collisions(nd, pd):
    total = 0
    negative_diagonals, positive_diagonals = nd[:], pd[:]
    for difference, queens in negative_diagonals:
        if queens > 1:
            total += queens - 1
    for difference, queens in positive_diagonals:
        if queens > 1:
            total += queens - 1
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


def swap_ok(i, j, nd, pd, play_board):
    board = play_board[:]
    negative_diagonals = nd[:]
    positive_diagonals = pd[:]
    # setup old differences and sums
    i_old_collisions = compute_collisions(list(d for d in negative_diagonals[0] if d[0] == (
        i - board[i])), list(d for d in positive_diagonals[0] if d[0] == (i + board[i])))
    j_old_collisions = compute_collisions(
        list(d for d in negative_diagonals[0] if d[0] == (j - board[j])), list(d for d in positive_diagonals[0] if d[0] == (j + board[j])))
    total_old = i_old_collisions + j_old_collisions

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
    nd = get_negative_diagonals(board)
    pd = get_positive_diagonals(board)
    cols = compute_collisions(nd[0], pd[0])
    return [board, nd, pd, cols]


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
        while loop < (c2 * size) and collisions != 0:
            # print("loop: {}\ncollisions: {}".format(
            #     loop, collisions))
            k = 0
            while k < number_of_attacks and collisions != 0:
                i = attack[k]
                j = random.randint(0, size-1)
                if swap_ok(i, j, negative_diagonals, positive_diagonals, board):
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
