class State:
    def __init__(self, instructions):
        self.acc = 0
        self.ptr = 0
        self.instructions = instructions
        self.visited_locations = []

    def run(self):
        while self.ptr < len(self.instructions):
            inst = self.instructions[self.ptr]

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
