lines = open("day13-input").read().splitlines()

target = int(lines[0])
lines = [
    int(line) if line != 'x' else -1
    for line in lines[1].split(',')
]


def part1(target, data):
    max_ts_id = -1
    max_ts = 9999999999999
    for item in data:
        ts = item * (target // item + 1)
        #print(item, ts - target)
        if ts < max_ts:
            max_ts_id = item
            max_ts = ts
    #print(max_ts_id, max_ts, (max_ts - target))
    return max_ts_id * (max_ts - target)


def is_valid(target, data):
    #print(len(data))
    if len(data) == 0:
        return True

    cur, rest = data[0], data[1:]
    if cur == -1:
        return is_valid(target + 1, rest)

    return target % cur == 0 and is_valid(target + 1, rest)


# Admittedly, chinese_remainder and mul_inv comes from Rosetta Code because I
# have no patience for this kind of problem.
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def part2(target, data):
    values = []
    remainders = []

    for i in range(len(data)):
        cur = data[i]
        if cur == -1:
            continue

        # We actually can't use i directly because the remainder of start
        # location is actually the inverse.
        values += [cur]
        remainders += [(cur-i)%cur]

    return chinese_remainder(values, remainders)


print(part1(target, list(filter(lambda x: x != -1, lines))))
print(part2(target, lines))

