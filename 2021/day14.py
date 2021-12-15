from collections import Counter

from adventlib import load_lines, split_lines

data = load_lines("day14-input")
template = data[0]
data = {line[0]: line[1] for line in split_lines(data[2:], sep=" -> ")}


doubles = Counter(template[i : i + 2] for i in range(len(template) - 1))


def calc(doubles):
    c = Counter()
    # For each double, add both letters to the counter. This will result in
    # double-counting every letter other than the first and last letter of the
    # sequence.
    for k, v in doubles.items():
        c[k[0]] += v
        c[k[1]] += v

    # Because the first and last letter of the template will never change, we
    # can add 1 to each of them to properly account for them (because everything
    # is doubled other than those 2, we add an extra to those to make everything
    # doubled)
    c[template[0]] += 1
    c[template[-1]] += 1

    # Loop throgh the counter and divide the results by 2 because everything is
    # double-counted. We use // rather than / to make sure we get ints, though
    # we'd get the same value either way.
    tmp = {v // 2 for k, v in c.items()}
    return max(tmp) - min(tmp)


for i in range(40):
    update = Counter()
    for k, v in doubles.items():
        if k in data:
            update[k] -= v
            update[k[0] + data[k]] += v
            update[data[k] + k[1]] += v
    doubles += update

    # Part 1 is at 10 iterations.
    if i == 9:
        print(calc(doubles))

print(calc(doubles))
