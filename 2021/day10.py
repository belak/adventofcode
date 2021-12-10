data = open("day10-input").read().splitlines()

point_lookup = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

part2_point_lookup = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

matches = {
    '{': '}',
    '[': ']',
    '(': ')',
    '<': '>',
}

def check_line(line):
    line = list(line)
    expected_stack = []
    unmatched = []

    while len(line) > 0:
        next_char, line = line[0], line[1:]

        if next_char in matches:
            expected_stack.append(matches[next_char])
            continue

        while len(expected_stack) > 0:
            expected = expected_stack.pop()
            if next_char == expected:
                break

            return (point_lookup[next_char], 0)

    while len(expected_stack) > 0:
        expected = expected_stack.pop()
        unmatched.append(expected)

    total = 0
    for m in unmatched:
        total = total * 5 + part2_point_lookup[m]

    return 0, total


total = 0
scores = []
for line in data:
    part1, part2 = check_line(line)
    total += part1
    scores.append(part2)

scores = list(sorted(filter(lambda x: x > 0, scores)))

print(total)
print(scores[len(scores) // 2])
