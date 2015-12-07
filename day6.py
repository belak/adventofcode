import re
from collections import defaultdict

matcher = re.compile('(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')

def on(v):
    return True

def off(v):
    return False

def toggle(v):
    return not v

ops = {
    'turn on': on,
    'turn off': off,
    'toggle': toggle,
}

def diff(num):
    def inner(v):
        x = v + num
        if x < 0:
            x = 0
        return x

    return inner

step2_ops = {
    'turn on': diff(1),
    'turn off': diff(-1),
    'toggle': diff(2),
}

def calculate_lights(ops):
    data = defaultdict(lambda: 0)

    for line in open('input/day6'):
        op, x1, y1, x2, y2 = matcher.match(line).groups()
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        f = ops[op]

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                data[(x, y)] = f(data[(x, y)])

    count = 0
    total = 0
    for e in data.values():
        total += e
        if e:
            count += 1

    return count, total

print(calculate_lights(ops))
print(calculate_lights(step2_ops))
