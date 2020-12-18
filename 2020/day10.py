lines = [int(line) for line in open("day10-input").read().splitlines()]
lines.append(0)
lines.sort()
lines.append(lines[len(lines) - 1] + 3)


def part1(data):
    one_count = 0
    three_count = 0

    for i in range(1, len(data)):
        diff = abs(data[i] - data[i - 1])
        if diff == 1:
            one_count += 1
        elif diff == 3:
            three_count += 1
        else:
            raise Exception(f"unknown diff: {diff}")

    return one_count * three_count


def part2(data):
    visited = {0: 1}

    for i in data[1:]:
        count = 0

        for j in range(1, 4):
            if i - j in visited:
                count += visited[i - j]

        visited[i] = count

    return visited[data[-1]]


print(part1(lines))
print(part2(lines))
