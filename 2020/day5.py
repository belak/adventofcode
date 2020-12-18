lines = [[line[:-3], line[-3:]] for line in open("day5-input").read().splitlines()]


def get_ids(data):
    ret = []

    for item in data:
        size = 128
        low_row = 0
        high_row = 127

        for char in item[0]:
            size /= 2
            if char == "F":
                high_row -= size
            elif char == "B":
                low_row += size
            else:
                raise Error("invalid char")

        assert low_row == high_row

        size = 8
        low_seat = 0
        high_seat = 7

        for char in item[1]:
            size /= 2
            if char == "R":
                low_seat += size
            elif char == "L":
                high_seat -= size
            else:
                raise Error("invalid char")

        assert low_seat == high_seat

        # print(low_row, low_seat)
        board_id = low_row * 8 + low_seat

        ret.append(board_id)

    ret.sort()

    return ret


def part1(data):
    return get_ids(data)[-1]


def part2(data):
    keys = get_ids(data)

    min_key = keys[0]
    max_key = keys[-1]

    for item in range(min_key, max_key):
        if item not in keys and item - 1 in keys and item + 1 in keys:
            return item

    return -1


print(part1(lines))
print(part2(lines))
