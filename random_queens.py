import random
min_range = [4, 100, 1000, 10000]
max_range = [99, 999, 9999, 99999]
queens_file = open("nqueens.txt", "w")
for i in range(4):
    for j in range(4):
        queens_file.write("{}\n".format(
            random.randint(min_range[i], max_range[i])))
queens_file.close()
