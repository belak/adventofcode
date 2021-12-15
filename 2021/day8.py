from adventlib import load_lines


data = load_lines("day8-input", lambda l: l.split(" | "))
data = [list(map(lambda x: x.split(" "), line)) for line in data]


# 1 == 2 segments
# 4 == 4 segments
# 7 == 3 segments
# 8 == 7 segments

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

count_map = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}

# 7 - 1 = a
# 4 + a =


def sort_str(data):
    return "".join(sorted(data))


count = 0

for line in data:
    for num in line[1]:
        if len(num) in count_map:
            # print(count_map[len(num)], num)
            count += 1

print(count)

total = 0
for patterns, output in data:
    patterns = [set(pattern) for pattern in patterns]

    # These 4 patterns are fairly easy, since they're unique lengths.
    one = next(filter(lambda x: len(x) == 2, patterns))
    seven = next(filter(lambda x: len(x) == 3, patterns))
    eight = next(filter(lambda x: len(x) == 7, patterns))
    four = next(filter(lambda x: len(x) == 4, patterns))

    # Each section is a grouping of a certain length, because it's an easy
    # characteristic to filter on. At this point, we need to look for the number
    # of intersections between the numbers.
    #
    # |   | 2 | 3 | 5 |
    # | 1 | 1 | 2 | 1 | # Because the overlap is unique here, we can determine 3
    # | 4 | 2 | x | 3 | # Because we can determine overlap for both 2 and 5, we're done after this

    three = next(
        filter(lambda x: len(x) == 5 and len(x.intersection(one)) == 2, patterns)
    )
    two = next(
        filter(
            lambda x: len(x) == 5 and len(x.intersection(four)) == 2 and x != three,
            patterns,
        )
    )
    five = next(
        filter(
            lambda x: len(x) == 5 and len(x.intersection(four)) == 3 and x != three,
            patterns,
        )
    )

    # Using the same method as above grouped by 6 segments.
    #
    # |   | 6 | 9 | 0 |
    # | 1 | 1 | 2 | 2 | # 6 intersecting with 1 is unique
    # | 4 | x | 4 | 3 | # This solves the last 2

    six = next(
        filter(lambda x: len(x) == 6 and len(x.intersection(one)) == 1, patterns)
    )
    nine = next(
        filter(
            lambda x: len(x) == 6 and len(x.intersection(four)) == 4 and x != six,
            patterns,
        )
    )
    zero = next(
        filter(
            lambda x: len(x) == 6 and len(x.intersection(four)) == 3 and x != six,
            patterns,
        )
    )

    str_count = len(
        set(
            [
                sort_str(one),
                sort_str(two),
                sort_str(three),
                sort_str(four),
                sort_str(five),
                sort_str(six),
                sort_str(seven),
                sort_str(eight),
                sort_str(nine),
                sort_str(zero),
            ]
        )
    )

    if str_count != 10:
        print(str_count)
        print(sort_str(two), sort_str(three), sort_str(five))
        print(sort_str(six), sort_str(nine), sort_str(zero))
    assert str_count == 10

    mapping = {
        sort_str(one): 1,
        sort_str(two): 2,
        sort_str(three): 3,
        sort_str(four): 4,
        sort_str(five): 5,
        sort_str(six): 6,
        sort_str(seven): 7,
        sort_str(eight): 8,
        sort_str(nine): 9,
        sort_str(zero): 0,
    }

    # print(mapping, output)
    addition = (
        1000 * mapping[sort_str(output[0])]
        + 100 * mapping[sort_str(output[1])]
        + 10 * mapping[sort_str(output[2])]
        + mapping[sort_str(output[3])]
    )
    total += addition

    # print(patterns, addition)

print(total)
