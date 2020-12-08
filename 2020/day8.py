lines = [
    line.split(' ', maxsplit=2)
    for line in open("day8-input").read().splitlines()
]


class State:
    def __init__(self, instructions):
        self.acc = 0
        self.ptr = 0
        self.instructions = instructions
        self.visited_locations = []

    def run(self):
        while self.ptr < len(self.instructions):
            inst = self.instructions[self.ptr]

            # print(self.ptr)
            # print(inst[0], inst[1])
            # print(int(inst[1]))

            prev_loc = self.ptr

            if self.ptr in self.visited_locations:
                return 'loop', self.acc

            if inst[0] == "nop":
                self.ptr += 1
            elif inst[0] == "acc":
                self.ptr += 1
                self.acc += int(inst[1])
            elif inst[0] == "jmp":
                self.ptr += int(inst[1])
            else:
                raise Exception(f'unknown instruction {inst[0]}')

            self.visited_locations += [prev_loc]

        return 'ok', self.acc


def part1(data):
    state = State(data)
    _, val = state.run()
    return val


def part2(data):
    for i in range(len(data)):
        if data[i][0] != "jmp":
            continue

        tmp = [line.copy() for line in data]
        tmp[i][0] = "nop"

        state = State(tmp)
        ok, acc = state.run()
        if ok == 'ok':
            return acc

    return None


print(part1(lines))
print(part2(lines))
