lines = open("day3-input").read().splitlines()


def slope(data, dx=3, dy=1):
    count = 0

    for i in range(len(data) // dy):
        x = i * dx
        y = i * dy
        item = data[y][x % len(data[y])]

        if item == "#":
            count += 1

    return count


part1 = slope(lines)
print(part1)

part2 = (
    slope(lines, dx=1, dy=1)
    * slope(lines, dx=3, dy=1)
    * slope(lines, dx=5, dy=1)
    * slope(lines, dx=7, dy=1)
    * slope(lines, dx=1, dy=2)
)
print(part2)
