from adventlib import load_lines


data = [int(line) for line in load_lines("day1-input")]

prev = None
increasing = 0

for line in data:
    cur = line

    if prev is not None:
        if cur > prev:
            increasing += 1

    prev = cur

print(increasing)

window_size = 3

prev = None
increasing = 0

for i in range(len(data) - window_size + 1):
    cur = sum(data[i: i + window_size])

    if prev is not None:
        if cur > prev:
            increasing += 1

    prev = cur

print(increasing)

