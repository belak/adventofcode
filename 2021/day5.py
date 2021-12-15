from numpy import sign  # why is this not in the stdlib

from adventlib import load_lines, split_lines

data = load_lines("day5-input", lambda l: l.split(" -> "))
data = [[elem.split(",") for elem in item] for item in data]
data = [[list(map(int, elem)) for elem in item] for item in data]


def calc(skip_func):
    output = {}

    for line in data:
        if skip_func(line):
            continue

        distance_x = line[1][0] - line[0][0]
        distance_y = line[1][1] - line[0][1]

        dx = sign(distance_x)
        dy = sign(distance_y)

        distance = max(abs(distance_x), abs(distance_y))

        for i in range(distance + 1):
            key = (line[0][0] + i * dx, line[0][1] + i * dy)
            if key not in output:
                output[key] = 0
            output[key] += 1

    return output


output = calc(lambda line: line[0][0] != line[1][0] and line[0][1] != line[1][1])
print(len(list(filter(lambda x: x >= 2, output.values()))))

output = calc(lambda _: False)
print(len(list(filter(lambda x: x >= 2, output.values()))))
