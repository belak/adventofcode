from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int


data = [line.split(" -> ") for line in open("day5-input").read().splitlines()]
data = [[elem.split(",") for elem in item] for item in data]
data = [[list(map(int, elem)) for elem in item] for item in data]
data = [[Point(x=elem[0], y=elem[1]) for elem in item] for item in data]

output = {}

for line in data:
    # Skip non horizontal/vertical lines
    if line[0].x != line[1].x and line[0].y != line[1].y:
        continue

    dx = 1
    dy = 1
    if line[0].x > line[1].x:
        dx = -1

    if line[0].y > line[1].y:
        dy = -1

    for x in range(line[0].x, line[1].x + dx, dx):
        for y in range(line[0].y, line[1].y + dy, dy):
            key = (x, y)
            # print(key)
            if key not in output:
                output[key] = 0
            output[key] += 1

# print(output)

print(len(list(filter(lambda x: x >= 2, output.values()))))

output = {}

for line in data:
    distance_x = line[0].x - line[1].x
    distance_y = line[0].y - line[1].y

    if distance_x < 0:
        dx = 1
    elif distance_x > 0:
        dx = -1
    else:
        dx = 0

    if distance_y < 0:
        dy = 1
    elif distance_y > 0:
        dy = -1
    else:
        dy = 0

    distance = max(abs(distance_x), abs(distance_y))
    print(line[0], line[1], distance)

    for i in range(distance + 1):
        key = (line[0].x + i * dx, line[0].y + i * dy)
        print(key)
        if key not in output:
            output[key] = 0
        output[key] += 1

for y in range(10):
    for x in range(10):
        print(output.get((x, y), "."), end="")
    print()


print(len(list(filter(lambda x: x >= 2, output.values()))))
