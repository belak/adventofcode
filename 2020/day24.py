from copy import copy
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def update_max(self, other):
        if other.x > self.x:
            self.x = other.x
        if other.y > self.y:
            self.y = other.y

    def update_min(self, other):
        if other.x < self.x:
            self.x = other.x
        if other.y < self.y:
            self.y = other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


OFFSETS = {
    "e": Point(1, 0),
    "se": Point(1, -1),
    "sw": Point(0, -1),
    "w": Point(-1, 0),
    "nw": Point(-1, 1),
    "ne": Point(0, 1),
}


def split_directions(line: str):
    ret = []
    while len(line) > 0:
        found = False
        for direction in OFFSETS.keys():
            if line.startswith(direction):
                ret += [direction]
                line = line[len(direction) :]
                found = True
                break
        if not found:
            raise Exception(f"failed to find direction: {line}")
    return ret


data = [split_directions(line) for line in open("day24-input").read().splitlines()]


def build_grid(data):
    grid = defaultdict(lambda: "w")
    for line in data:
        offset = Point(0, 0)
        for direction in line:
            offset += OFFSETS[direction]

        if grid[offset] == "w":
            grid[offset] = "b"
        else:
            grid[offset] = "w"

    return grid


def part1(data):
    grid = build_grid(data)
    return len(list(filter(lambda x: x == "b", grid.values())))


def part2(data):
    grid = build_grid(data)

    min_point = Point(0, 0)
    max_point = Point(0, 0)

    for point in grid.keys():
        min_point.update_min(point)
        max_point.update_max(point)

    # print(min_point, max_point)

    # 100 steps
    for step in range(1, 101):
        print(f'{step}%', end='\r')

        prev_grid = copy(grid)

        for x in range(min_point.x - 1, max_point.x + 2):
            for y in range(min_point.y - 1, max_point.y + 2):
                target = Point(x, y)
                black = 0
                for direction in OFFSETS.values():
                    offset = target + direction
                    if prev_grid[offset] == "b":
                        black += 1

                if prev_grid[target] == "b":
                    if black == 0 or black > 2:
                        grid[target] = "w"
                else:
                    if black == 2:
                        grid[target] = "b"

                # We should only need to update when the target is now black.
                if grid[target] == "b":
                    min_point.update_min(target)
                    max_point.update_max(target)

        # print(step + 1, len(list(filter(lambda x: x == "b", grid.values()))))
        # print(min_point, max_point)

    return len(list(filter(lambda x: x == "b", grid.values())))


print("part1:", part1(data))
print("part2:", part2(data))
