data = [int(line) for line in open('day1-input').read().splitlines()]

prev = None
increasing = 0
decreasing = 0
same = 0

for line in data:
    cur = line

    if prev is not None:
        if cur > prev:
            increasing += 1
        elif cur < prev:
            decreasing += 1
        else:
            same += 1

    prev = cur

print(increasing, decreasing, same)

window_size = 3

prev = None
increasing = 0
decreasing = 0
same = 0

for i in range(len(data) - window_size + 1):
    cur = data[i: i + window_size]

    if prev is not None:
        cur_sum = sum(cur)
        prev_sum = sum(prev)

        if cur_sum > prev_sum:
            increasing += 1
        elif cur_sum < prev_sum:
            decreasing += 1
        else:
            same += 1

    prev = cur

print(increasing, decreasing, same)

