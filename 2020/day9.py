lines = [int(line) for line in open("day9-input").read().splitlines()]


def check_number(window, num):
    for i in window:
        for j in window:
            if i + j == num:
                return True

    return False


def part1(data):
    idx = 0
    for item in data[25:]:
        window = data[idx : idx + 25]
        if not check_number(window, item):
            return item

        idx += 1

    return -1


def part2(data):
    target = part1(data)
    for i in range(len(data)):
        for j in range(len(data[i:])):
            window = data[i:j]
            total = sum(window)
            if total == target:
                return min(window) + max(window)
            elif total > target:
                break

    return -1


print(part1(lines))
print(part2(lines))
