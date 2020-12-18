lines = [line.splitlines() for line in open("day6-input").read().split("\n\n")]


def part1(data):
    total = 0
    for group in data:
        group_questions = set()

        for person in group:
            for letter in person:
                group_questions.add(letter)

        total += len(group_questions)

    return total


def part2(data):
    total = 0
    for group in data:
        group_questions = set(group[0])

        for person in group:
            for item in group[0]:
                if item not in person:
                    group_questions.discard(item)

        total += len(group_questions)

    return total


print(part1(lines))
print(part2(lines))
