import numpy as np

data = open("day13-input").read().split("\n\n")
data, folds = data[0], data[1]
data = [list(map(int, line.split(","))) for line in data.splitlines()]
folds = [line.removeprefix("fold along ") for line in folds.splitlines()]
folds = [line.split("=") for line in folds]
folds = [(line[0], int(line[1])) for line in folds]

max_x = 0
max_y = 0
for (x, y) in data:
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

arr = np.zeros((max_y + 1, max_x + 1), dtype=int)
for (x, y) in data:
    arr[y, x] = 1


def print_arr(arr):
    for y in range(len(arr)):
        for x in range(len(arr[0])):
            v = arr[y, x]
            if v:
                print("#", end="")
            else:
                print(".", end="")
        print()


def process_fold(arr, fold):
    axis, coord = fold
    if axis == "y":
        for y in range(len(arr) - coord - 1):
            for x in range(len(arr[0])):
                if arr[coord + y + 1, x] == 1:
                    arr[coord - y - 1, x] = 1
        while len(arr) > coord:
            arr = np.delete(arr, coord, axis=0)
    else:
        for x in range(len(arr[0]) - coord - 1):
            for y in range(len(arr)):
                if arr[y, coord + x + 1] == 1:
                    arr[y, coord - x - 1] = 1
        while len(arr[0]) > coord:
            arr = np.delete(arr, coord, axis=1)
    return arr

count = 0
arr = process_fold(arr, folds[0])
for line in arr:
    for c in line:
        if c == 1:
            count += 1
print(count)

for fold in folds[1:]:
    arr = process_fold(arr, fold)

print_arr(arr)
