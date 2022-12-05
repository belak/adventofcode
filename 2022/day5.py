import re

from adventlib import AOC

MOVEMENT_RE = re.compile(r"move (\d+) from (\d+) to (\d+)")


class Crane:
    def __init__(self, name):
        self.name = name
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def __repr__(self):
        return "Crane<{}, {}>".format(self.name, self.stack)


def parse_cranes(crane_data):
    names, crane_data = crane_data[0].strip().split(), crane_data[1:]
    cranes = [Crane(name) for name in names]
    for line in crane_data:
        for (i, _) in enumerate(cranes):
            col = 1 + 4 * i
            try:
                item = line[col].strip()
                if item:
                    cranes[i].push(item)
            except IndexError:
                pass
    return cranes


def parse_movements(movements):
    return [tuple(map(int, MOVEMENT_RE.findall(movement)[0])) for movement in movements]


class Day5(AOC):
    def process_input(self, raw_data):
        [crane_data, movements] = raw_data.split("\n\n")
        crane_data = crane_data.splitlines()
        crane_data.reverse()
        movements = movements.splitlines()

        self.cranes = crane_data
        self.movements = movements

    def part1(self):
        cranes = parse_cranes(self.cranes)
        movements = parse_movements(self.movements)
        for (x, src, dest) in movements:
            src = src - 1
            dest = dest - 1
            for _ in range(x):
                item = cranes[src].pop()
                cranes[dest].push(item)

        ret = ""
        for c in cranes:
            ret += c.peek()

        return ret

    def part2(self):
        cranes = parse_cranes(self.cranes)
        movements = parse_movements(self.movements)
        for (x, src, dest) in movements:
            src = src - 1
            dest = dest - 1

            # Pop off n items, reverse them, and push them onto the dest. It
            # should be the same as moving n items from src to dest.
            items = []
            for _ in range(x):
                items.append(cranes[src].pop())

            items.reverse()

            for item in items:
                cranes[dest].push(item)

        ret = ""
        for c in cranes:
            ret += c.peek()

        return ret


if __name__ == "__main__":
    aoc = Day5()
    aoc.run()
