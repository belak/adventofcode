from numpy import ndarray

from adventlib import AOC, print_arr


CMD_DELAY = {
    "addx": 2,
    "noop": 0,
}


class CPU:
    def __init__(self, cmds):
        self.cycle = 1
        self.x = 1
        self.queue = cmds
        self.current_cmd = None
        self.current_delay = 0

    def pre(self):
        if self.current_cmd is not None or not self.queue:
            return

        self.current_cmd = self.queue[0]
        self.current_delay = CMD_DELAY[self.current_cmd[0]]
        self.queue = self.queue[1:]

    def post(self):
        self.cycle += 1
        self.current_delay -= 1

        if self.current_cmd is None or self.current_delay > 0:
            return

        if self.current_cmd[0] == "noop":
            pass
        elif self.current_cmd[0] == "addx":
            self.x += self.current_cmd[1]
        else:
            raise Exception("unknown cmd: {}".format(self.current_cmd[0]))

        self.current_cmd = None


class Day10(AOC):
    def process_input(self, raw_data):
        raw_data = [line.split(" ") for line in raw_data.splitlines()]
        instructions = []
        for line in raw_data:
            if line[0] == "addx":
                instructions.append(("addx", int(line[1])))
            elif line[0] == "noop":
                instructions.append(("noop",))
        return instructions

    def part1(self):
        total = 0
        cpu = CPU(self.data)

        for _ in range(220):
            cpu.pre()
            if cpu.cycle in [20, 60, 100, 140, 180, 220]:
                total += cpu.cycle * cpu.x
            cpu.post()
        return total

    def part2(self):
        grid = ndarray((6, 40), int)
        cpu = CPU(self.data)

        for _ in range(240):
            cpu.pre()
            pixel = cpu.cycle - 1
            x = pixel % 40
            y = pixel // 40
            grid[y, x] = (1 if abs(x-cpu.x) <= 1 else 0)
            cpu.post()

        print_arr(grid)


if __name__ == "__main__":
    aoc = Day10()
    aoc.run()
