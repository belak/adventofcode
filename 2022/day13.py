from json import loads

from adventlib import AOC


# Shove everything into a wrapper class and implement __lt__ so we can sort
# these values directly.
class Val:
    def __init__(self, data):
        self.data = loads(data)

    def __lt__(self, other):
        return check_value(self.data, other.data)

    def __repr__(self):
        return '{}'.format(self.data)


def check_value(left, right):
    # print('- Compare {} vs {}'.format(left, right))
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            # print("Left side is smaller, so inputs are in the right order")
            return True
        elif left > right:
            # print("Right side is smaller, so inputs are not in the right order")
            return False
        else:
            return None
    elif isinstance(left, list) and isinstance(right, list):
        try:
            for i in range(max(len(left), len(right)) + 1):
                val = check_value(left[i], right[i])
                if val is None:
                    continue
                elif val:
                    return True
                else:
                    return False
            raise Exception('got to end of list without a decision')
        except IndexError:
            if len(left) < len(right):
                # print("Left side ran out of items, so inputs are in the right order")
                return True
            elif len(left) > len(right):
                # print("Right side ran out of items, so inputs are not in the right order")
                return False
            else:
                return None
    elif isinstance(left, int):
        left = [left]
        # print("- Mixed types; convert left to {} and retry comparison".format(left))
        return check_value(left, right)
    elif isinstance(right, int):
        right = [right]
        # print("- Mixed types; convert right to {} and retry comparison".format(left))
        return check_value(left, right)
    else:
        raise Exception("unknown mix of types")


class Day13(AOC):
    def process_input(self, raw_data):
        return [list(map(Val, group.splitlines())) for group in raw_data.split("\n\n")]

    def part1(self):
        total = 0
        for (i, [left, right]) in enumerate(self.data, 1):
            # print('== Pair {} =='.format(i))
            if check_value(left.data, right.data):
                total += i
        return total

    def part2(self):
        d1 = Val('[[2]]')
        d2 = Val('[[6]]')
        items = [d1, d2]
        for (left, right) in self.data:
            items.append(left)
            items.append(right)
        items.sort()

        mul = 1
        for (i, val) in enumerate(items, 1):
            if val == d1 or val == d2:
                mul *= i
        return mul


if __name__ == "__main__":
    aoc = Day13()
    aoc.run()
