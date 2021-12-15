import numpy as np


CARDINAL_DIRS = [
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0),
]

ORDINAL_DIRS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (1, -1),
    (1, 1),
    (-1, 0),
    (-1, 1),
    (-1, -1),
]


def print_arr(arr, max_x=float("inf"), max_y=float("inf")):
    """
    Print a 2d array, using . for falsy values and # for truthy.

    This also accepts optional max_x and max_y arguments to display only a
    portion of the array.
    """
    coords = (min(max_x, len(arr[0])), min(max_y, len(arr)))
    for y in range(coords[1]):
        for x in range(coords[0]):
            print("#" if arr[y, x] else ".", end="")
        print()


def truncate_arr(arr, max_x, max_y):
    """
    Truncate a 2d array to given x and y values.
    """
    arr = np.delete(arr, list(range(max_y, len(arr))), axis=0)
    arr = np.delete(arr, list(range(max_x, len(arr[0]))), axis=1)
    return arr


def parse_2d_grid(data):
    data = [str_to_ints(line) for line in data.splitlines()]
    return np.array(data)


def load_2d_grid(filename):
    with open(filename) as f:
        data = f.read()
        return parse_2d_grid(data)


def load_lines(filename, cast=None):
    with open(filename) as f:
        data = f.read().splitlines()

        if cast is not None:
            data = [cast(line) for line in data]

        return data


def load_sections(filename):
    return load_list(filename, sep="\n\n")


def split_lines(data, sep=","):
    return [line.split(sep) for line in data]


def load_list(filename, sep=",", cast=int):
    with open(filename) as f:
        return list(map(cast, f.read().split(sep)))


def str_to_ints(data):
    return list(map(int, data))
