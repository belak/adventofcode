import re
from functools import cmp_to_key

(data1, data2) = open("./input-5").read().split("\n\n")
data1 = [tuple(map(int, line.split("|"))) for line in data1.splitlines()]
data2 = [tuple(map(int, line.split(","))) for line in data2.splitlines()]

data1lookup = {}
for p1, p2 in data1:
    data1lookup[p1] = data1lookup.get(p1, []) + [(p1, p2)]
    data1lookup[p2] = data1lookup.get(p2, []) + [(p1, p2)]

total = 0
total2 = 0


def custom_cmp(x, y, rules):
    if (x, y) in rules:
        return -1
    if (y, x) in rules:
        return 1

    return 0


for update in data2:
    # Find all relevant rules
    rules = set()
    for num in update:
        for r0, r1 in data1lookup.get(num, None):
            if r0 not in update or r1 not in update:
                continue

            rules.add((r0, r1))

    # Check each rule against this update
    valid = True
    for rule in rules:
        idx0 = update.index(rule[0])
        idx1 = update.index(rule[1])
        if idx0 > idx1:
            valid = False
            break

    if valid:
        total += update[len(update) // 2]
    else:
        key_func = cmp_to_key(lambda x, y: custom_cmp(x, y, rules))
        new_update = sorted(update, key=key_func)
        total2 += new_update[len(new_update) // 2]


print(total)
print(total2)
