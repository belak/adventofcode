import numpy as np


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
