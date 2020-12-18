from aoc.asm import State


lines = [line.split(" ", maxsplit=2) for line in open("day8-input").read().splitlines()]


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
        if ok == "ok":
            return acc

    return None


print(part1(lines))
print(part2(lines))
