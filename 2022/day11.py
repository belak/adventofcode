from math import lcm

from adventlib import AOC

# Monkey 0:
#  Starting items: 79, 98
#  Operation: new = old * 19
#  Test: divisible by 23
#    If true: throw to monkey 2
#    If false: throw to monkey 3


class Monkey:
    def __init__(self, data):
        lines = data.splitlines()
        self.name = lines[0].removesuffix(":")
        self.items = list(
            map(int, lines[1].strip().removeprefix("Starting items: ").split(", "))
        )
        self.operation = (
            lines[2].strip().removeprefix("Operation: new = old ").split(" ")
        )
        self.test = int(lines[3].strip().removeprefix("Test: divisible by "))
        self.if_true = int(lines[4].strip().removeprefix("If true: throw to monkey "))
        self.if_false = int(lines[5].strip().removeprefix("If false: throw to monkey "))
        self.inspected = 0

    def push(self, *items):
        self.items.extend(items)

    def step(self, global_lcm=None):
        ret = {}
        for item in self.items:
            self.inspected += 1
            op_amount = item if self.operation[1] == "old" else int(self.operation[1])
            if self.operation[0] == "*":
                item = item * op_amount
            elif self.operation[0] == "+":
                item = item + op_amount

            if global_lcm is None:
                item = item // 3
            elif item > global_lcm:
                item = item % global_lcm

            if item % self.test == 0:
                if self.if_true not in ret:
                    ret[self.if_true] = []
                ret[self.if_true].append(item)
            else:
                if self.if_false not in ret:
                    ret[self.if_false] = []
                ret[self.if_false].append(item)

        self.items = []

        return ret


class Day11(AOC):
    def process_input(self, raw_data):
        return [Monkey(line) for line in raw_data.split("\n\n")]

    def part1(self):
        for _ in range(20):
            for monkey in self.data:
                throws = monkey.step()

                for k, v in throws.items():
                    self.data[k].push(*v)

        data = [monkey.inspected for monkey in self.data]
        data.sort()

        return data[-1] * data[-2]

    def part2(self):
        global_lcm = lcm(*[monkey.test for monkey in self.data])
        for i in range(10000):

            if (i < 1000 and (i + 1) % 100 == 0) or (i + 1) % 1000 == 0:
                print(i + 1)
            for monkey in self.data:
                throws = monkey.step(global_lcm=global_lcm)
                for k, v in throws.items():
                    self.data[k].push(*v)

        data = [monkey.inspected for monkey in self.data]
        data.sort()

        return data[-1] * data[-2]


if __name__ == "__main__":
    aoc = Day11()
    aoc.run()
