from adventlib import load_lines


data = load_lines("day2-input", lambda l: l.split())
data = [(line[0], int(line[1])) for line in data]

depth = 0
pos = 0

for (direction, amount) in data:
    if direction == "forward":
        pos += amount
    elif direction == "down":
        depth += amount
    elif direction == "up":
        depth -= amount
    else:
        raise Exception("unknown direction: %s" % direction)

print(depth * pos)

depth = 0
pos = 0
aim = 0

for (direction, amount) in data:
    if direction == "forward":
        pos += amount
        depth += aim * amount
    elif direction == "down":
        aim += amount
    elif direction == "up":
        aim -= amount
    else:
        raise Exception("unknown direction: %s" % direction)

print(depth * pos)
