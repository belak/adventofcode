from itertools import chain, combinations

ONES = int('1' * 36, 2)
ZERO = int('0' * 36, 2)

lines = [
    line.split(' = ')
    for line in open("day14-input").read().splitlines()
]

for line in lines:
    if line[0] == 'mask':
        zero_mask = int(line[1].replace('X', '1'), 2)
        ones_mask = int(line[1].replace('X', '0'), 2)
        x_mask = line[1].replace('0', ' ').replace('1', ' ')
        line[1] = (zero_mask, ones_mask, x_mask)
    else:
        line[0] = int(line[0][4:-1])
        line[1] = int(line[1])


# From https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def part1(data):
    mask = (ONES, ZERO)

    mem = {}
    for line in data:
        pos = line[0]
        if pos == 'mask':
            mask = line[1]
        else:
            val = (line[1] | mask[1]) & mask[0]
            mem[pos] = val

    return sum(mem.values())


def part2(data):
    mask = (ZERO, ZERO, ZERO)

    mem = {}
    for line in data:
        if line[0] == 'mask':
            mask = line[1]
        else:
            pos = line[0] | mask[1]
            # NOTE: Bit addresses are most significant bit first, but with how
            # we bitmask below, we start with least significant bit, so we
            # reverse it here.
            x_locs = [35 - i for i, val in enumerate(mask[2]) if val == 'X']

            # Iterate over all possible sets of bits which changed, so we can
            # change them.
            for change in powerset(x_locs):
                diff = 0
                for bit in change:
                    diff |= (1 << bit)
                mem[pos ^ diff] = line[1]

    return sum(mem.values())


print('part1:', part1(lines))
print('part2:', part2(lines))
