from math import floor, ceil

from adventlib import AOC


class Node:
    def __init__(self, val, depth=-1):
        self.val = val
        self.depth = depth

    def magnitude(self):
        if isinstance(self.val, int):
            return self.val

        return 3 * self.val[0] + 2 * self.val[1]

    def set_depth(self, depth):
        self.depth = depth
        if isinstance(self.val, list):
            for node in self.val:
                node.set_depth(depth + 1)

    def __repr__(self):
        # return "Node({})<{}>".format(self.depth, self.val)
        return "{}".format(self.val)

    def __iter__(self):
        yield self
        if isinstance(self.val, list):
            for node in self.val:
                yield from node


def try_explode(nodes):
    prev_num = None
    next_num = None
    target = None

    skip = 2

    for node in nodes:
        if isinstance(node.val, int):
            if target is None:
                prev_num = node
            elif skip >= 0:
                next_num = node
                skip -= 1
            else:
                break
            continue

        if node.depth > 4 and all(map(lambda x: isinstance(x.val, int), node.val)):
            target = node

    if target is None:
        return False

    if prev_num is not None:
        prev_num.val += target.val[0].val
    if next_num is not None:
        next_num.val += target.val[1].val
    target.val = 0

    return True


def try_split(nodes):
    for node in nodes:
        if isinstance(node.val, int) and node.val >= 10:
            node.val = [
                Node(floor(node.val / 2), node.depth + 1),
                Node(ceil(node.val / 2), node.depth + 1),
            ]
            return True

    return False


def parse_snail(lines):
    return Node(
        [parse_snail(line) if isinstance(line, list) else Node(line) for line in lines],
    )


class Day18(AOC):
    def process_input(self, raw_data):
        return [parse_snail(eval(line)) for line in raw_data.splitlines()]

    def part1(self):
        final = self.data[0]
        for line in self.data[1:]:
            print("have", final)
            print("adding", line)
            node = Node([final, line])
            node.set_depth(1)

            while True:
                if try_explode(node):
                    print("after exp: ", node)
                    continue
                if try_split(node):
                    print("after spl: ", node)
                    continue
                break

            final = node

        print(final)

        return final.magnitude()

    def part2(self):
        pass


if __name__ == "__main__":
    aoc = Day18()
    aoc.run()
