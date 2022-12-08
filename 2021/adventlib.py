from copy import deepcopy
import time
import inspect
from pathlib import Path
from contextlib import contextmanager

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


def split_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def print_arr(arr, max_x=float("inf"), max_y=float("inf")):
    """
    Print a 2d array, using space for falsy values and # for truthy.

    This also accepts optional max_x and max_y arguments to display only a
    portion of the array.
    """
    coords = (min(max_x, len(arr[0])), min(max_y, len(arr)))
    for y in range(coords[1]):
        for x in range(coords[0]):
            print("#" if arr[y, x] else " ", end="")
        print()


def truncate_arr(arr, max_x, max_y):
    """
    Truncate a 2d array to given x and y values.
    """
    arr = np.delete(arr, list(range(max_y, len(arr))), axis=0)
    arr = np.delete(arr, list(range(max_x, len(arr[0]))), axis=1)
    return arr


def parse_2d_grid(data):
    data = [concrete_map(line) for line in data.splitlines()]
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


def concrete_map(data, cast=int):
    return list(map(cast, data))


def window(data, n):
    for i in range(len(data) - n + 1):
        yield data[i : i + n]


@contextmanager
def timer(name):
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end - start:.2f}s")


class AOC:
    def __init__(self):
        if getattr(self, "input_filename", None) is None:
            self.input_filename = (
                Path(inspect.getfile(type(self))).with_suffix("").name + "-input"
            )

    def run(self):
        self.load_input()
        with timer("process_input"):
            data = self.process_input(self.raw_data)
            if data is not None:
                self.raw_data = data

        with timer("part1"):
            self.data = deepcopy(self.raw_data)
            part1 = self.part1()
            if part1 is not None:
                print(part1)

        with timer("part2"):
            self.data = deepcopy(self.raw_data)
            part2 = self.part2()
            if part2 is not None:
                print(part2)

        self.finalize()

    def load_input(self):
        with open(self.input_filename) as f:
            self.raw_data = f.read().strip("\n")

    def process_input(self, raw_data):
        raise NotImplementedError

    # Overrides below here
    def part1(self):
        raise NotImplementedError

    def part2(self):
        raise NotImplementedError

    def finalize(self):
        pass
