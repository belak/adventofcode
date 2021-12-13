import numpy as np

from adventlib import print_arr, truncate_arr

data = open("day13-input").read().split("\n\n")
data, folds = data[0], data[1]
data = [list(map(int, line.split(","))) for line in data.splitlines()]
folds = [line.removeprefix("fold along ") for line in folds.splitlines()]
folds = [line.split("=") for line in folds]
folds = [(line[0], int(line[1])) for line in folds]

# Split the input into arrays of x and y values so we can find the max coord.
x_vals, y_vals = list(zip(*data))
max_x = max(x_vals)
max_y = max(y_vals)

# Create a new empty array and fill it up
arr = np.zeros((max_y + 1, max_x + 1), dtype=int)
for (x, y) in data:
    arr[y, x] = 1


def process_fold(arr, max_x, max_y, fold):
    axis, coord = fold
    if axis == "y":
        for y in range(max_y - coord - 1):
            for x in range(max_x):
                if arr[coord + y + 1, x] == 1:
                    arr[coord - y - 1, x] = 1
        max_y = coord
    else:
        for x in range(max_x - coord - 1):
            for y in range(max_y):
                if arr[y, coord + x + 1] == 1:
                    arr[y, coord - x - 1] = 1
        max_x = coord
    return max_x, max_y


max_x, max_y = process_fold(arr, max_x, max_y, folds[0])
arr = truncate_arr(arr, max_x, max_y)
count = np.count_nonzero(arr)
print(count)

for fold in folds[1:]:
    max_x, max_y = process_fold(arr, max_x, max_y, fold)

arr = truncate_arr(arr, max_x, max_y)

print_arr(arr)
