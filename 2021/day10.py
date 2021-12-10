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

def check_line(line, idx=0, expected_stack=None):
    if expected_stack is None:
        expected_stack = []

    if len(line) == 0:
        return

    next_char, rest = line[0], line[1:]

    if next_char in matches:
        expected_stack.append(matches[next_char])
        return check_line(rest, idx+1, expected_stack)
    else:
        expected = expected_stack.pop()
        if next_char == expected:
            return check_line(rest, idx+1, expected_stack)
        else:
            return idx

def check_line_part2(line):
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

            unmatched.append(expected)

    while len(expected_stack) > 0:
        expected = expected_stack.pop()
        unmatched.append(expected)

    total = 0
    for m in unmatched:
        total = total * 5 + part2_point_lookup[m]
    return total


total = 0
scores = []
for line in data:
    idx = check_line(line)
    if idx is not None:
        total += point_lookup[line[idx]]
    else:
        scores.append(check_line_part2(line))



print(total)
scores.sort()
print(scores[len(scores) // 2])
