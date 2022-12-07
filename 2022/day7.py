import math

from adventlib import AOC


TOTAL_SPACE = 70000000
TARGET_UNUSED = 30000000
TARGET = TOTAL_SPACE - TARGET_UNUSED


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}

    def get_child(self, name):
        if name not in self.children:
            child = Dir(name, self)
            self.children[name] = child
        return self.children[name]

    def size(self):
        return sum([
            child.size() if isinstance(child, Dir) else child
            for child in self.children.values()
        ])

    def __repr__(self):
        return "Dir<{}>".format(self.name)

    def __iter__(self):
        yield self
        for val in self.children.values():
            if isinstance(val, Dir):
                yield from val


class Cmd:
    def __init__(self, data):
        lines = [line.split(" ") for line in data.splitlines()]
        self.cmd = lines[0][0]
        self.arg = ''
        if len(lines[0]) > 1:
            self.arg = lines[0][1]
        self.output = lines[1:]

    def __repr__(self):
        return "Cmd<{}, {}>".format(self.cmd, self.arg)


class Day7(AOC):
    def process_input(self, raw_data):
        cmds = [Cmd(line) for line in raw_data.removeprefix("$ ").split("\n$ ")]

        # The first cmd always seems to be "cd /", so we ignore it for easier
        # processing and make the root node ourselves.
        assert cmds[0].cmd == "cd"
        assert cmds[0].arg == "/"

        root = Dir('/')
        cur = root

        for cmd in cmds[1:]:
            if cmd.cmd == "cd":
                if cmd.arg == "..":
                    cur = cur.parent
                else:
                    cur = cur.get_child(cmd.arg)
            elif cmd.cmd == "ls":
                for line in cmd.output:
                    if line[0] == 'dir':
                        cur.get_child(line[0])
                    else:
                        cur.children[line[1]] = int(line[0])
            else:
                raise Exception("unknown cmd: {}".format(cmd.cmd))

        return root

    def part1(self):
        total = 0
        for node in self.data:
            size = node.size()
            if size < 100000:
                total += size
        return total

    def part2(self):
        smallest = math.inf
        used = self.data.size()
        for node in self.data:
            size = node.size()
            if used - size < TARGET and size < smallest:
                smallest = size
        return smallest


if __name__ == "__main__":
    aoc = Day7()
    aoc.run()
