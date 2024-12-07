data = [line.split(": ") for line in open("./input-7").readlines()]
data = [(int(line[0]), list(map(int, line[1].split(" ")))) for line in data]


total = 0
total2 = 0

queue = data


# This is roughly based off the answer in https://stackoverflow.com/a/54054183,
# but we went with a combination of fastest and easiest to understand. Also, the
# results in that answer don't line up with real world python any more, so take
# them with a grain of salt, but they're a good starting point.
def int_len(i):
    return len(str(i))


def concat_ints(i1, i2):
    return i1 * (10 ** int_len(i2)) + i2


def process_eqn(target, equation, ops, sum=None):
    if len(equation) == 0:
        if sum == target:
            return target

        return None

    first, equation = equation[0], equation[1:]

    if sum is None:
        return process_eqn(target, equation, ops, first)

    for op in ops:
        if op == "+":
            new_sum = sum + first
        elif op == "*":
            new_sum = sum * first
        elif op == "||":
            new_sum = concat_ints(sum, first)

        # print("recurse:", (target, new_sum, equation))
        if process_eqn(target, equation, ops, new_sum):
            return target

    return False


p1ops = ["+", "*"]
total = sum([int(process_eqn(target, equation, p1ops)) for (target, equation) in data])

print(total)

p2ops = ["+", "*", "||"]

for i, (target, equation) in enumerate(data):
    # print(i, len(data))
    total2 += int(process_eqn(target, equation, p2ops))

print(total2)
