import time


def take_input():
    # Accepts the size of the chess board
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


# Main class, execution
def solve_n_queens(n):
    start = time.time()
    result = (solve_for_n_queens(n, 0, []))
    end = time.time()
    print(end - start)
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

    print('Result: ')
    print(result)


# Algorithm
def solve_for_n_queens(n, row, col_placements):
    # If end is reached, return result
    if row == n:
        return col_placements
    else:
        # For loop ensure no queen shares row
        for col in range(0, n):
            # Ensure no queen shares col
            if col not in col_placements:
                col_placements.append(col)
                # Use helper function to check diagonals
                if is_valid(col_placements):
                    result = solve_for_n_queens(n, row + 1, col_placements)
                    # Break out of loop if a solution is found
                    if result:
                        return result
                col_placements.pop(len(col_placements) - 1)


def is_valid(col_placements):
    if len(col_placements) == 1:
        return True
    most_recent_queen = len(col_placements) - 1
    for existingQueen in range(0, most_recent_queen):
        # Diagonal checks
        if col_placements[existingQueen] > col_placements[most_recent_queen]:
            if (col_placements[existingQueen] + existingQueen) ==\
                    (col_placements[most_recent_queen] + most_recent_queen):
                return False
        elif (col_placements[existingQueen] - existingQueen) ==\
                (col_placements[most_recent_queen] - most_recent_queen):
                return False
    return True


# n = take_input()
n = 30
print('Processing...')
solve_n_queens(n)
