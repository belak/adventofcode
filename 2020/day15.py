data = list(map(int, open("day15-input").read().split(',')))


def calculate(data, target):
    last_seen = {}

    last_num = 0
    idx = 0

    for item in data:
        last_seen[item] = idx
        last_num = item
        idx += 1

    while idx < target:
        # Basic progress that won't slow down the calculation
        if idx % 1000000 == 0:
            print(idx)

        last_num_idx = last_seen.get(last_num)
        last_seen[last_num] = idx - 1
        if last_num_idx is None:
            last_num = 0
        else:
            last_num = (idx - 1) - last_num_idx

        idx += 1

    return last_num


def part1(data):
    return calculate(data, 2020)


def part2(data):
    return calculate(data, 30000000)


print('part1:', part1(data))
print('part2:', part2(data))
