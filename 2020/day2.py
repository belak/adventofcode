lines = [line.split(" ", 3) for line in open("day2-input").read().splitlines()]
lines = [(map(int, line[0].split("-", 2)), line[1][:-1], line[2]) for line in lines]


def part1():
    count = 0
    for line in lines:
        if line[0][0] <= line[2].count(line[1]) <= line[0][1]:
            count += 1
    return count


def part2():
    count = 0
    for line in lines:
        found1 = False
        found2 = False

        if line[2][line[0][0] - 1] == line[1]:
            found1 = True

        if line[2][line[0][1] - 1] == line[1]:
            found2 = True

        if (found1 and not found2) or (found2 and not found1):
            count += 1

    return count


print(part1())
print(part2())
