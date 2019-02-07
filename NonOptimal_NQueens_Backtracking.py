import time

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

def solveNQueens(n):
    start = time.time()
    print(solveForNQueens(n, 0, []))
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

def solveForNQueens(n, row, colPlacements):
    if row == n:
        return colPlacements
    else:
        for col in range(0, n):
            colPlacements.append(col)
            if isValid(colPlacements):
                result = solveForNQueens(n, row + 1, colPlacements)
                if result:
                    return result
            colPlacements.pop(len(colPlacements) - 1)

def isValid(colPlacements):
    rowValidating = len(colPlacements) - 1
    for ithQueenRow in range(0, rowValidating):
        absoluteColDistance = abs(colPlacements[ithQueenRow] - colPlacements[rowValidating])
        if absoluteColDistance == 0 or absoluteColDistance == (rowValidating - ithQueenRow):
            return False
    return True

n = take_input()
solveNQueens(n)
