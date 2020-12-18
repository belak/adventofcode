data = [
    line.split(" ")
    for line in open("day18-input")
    .read()
    .replace("(", "( ")
    .replace(")", " )")
    .splitlines()
]


class Calculator:
    OPS = {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
    }

    def __init__(self, data, mode=1):
        self.data = data
        self.mode = mode

    def parse_value(self, data):
        item, rest = data[0], data[1:]
        if item == "(":
            expr, rest = self.split_inner_expr(rest)
            return self.parse_expr(expr), rest
        else:
            return int(item), rest

    def split_inner_expr(self, line):
        depth = 1
        i = 0
        for item in line:
            i += 1
            if item == "(":
                depth += 1
            elif item == ")":
                depth -= 1

            if depth == 0:
                return line[: i - 1], line[i:]

        raise Exception("mismatched parens")

    def parse_expr(self, data):
        # Start by flattening out this array - calculate any nested parens as a value.
        total, rest = self.parse_value(data)
        tmp = [total]
        while len(rest) > 0:
            arg, rest = rest[0], rest[1:]
            val, rest = self.parse_value(rest)
            tmp += [arg, val]
        rest = tmp

        if self.mode == 1:
            precidence = ["+*"]
        else:
            precidence = ["+", "*"]

        # Essentially, do a pass for each op set (in order of precidence) to
        # reduce the array. When we get to the end, we should have 1 element
        # in the list.
        for valid_ops in precidence:
            i = 0
            while (2 * i) + 1 < len(rest):
                idx = (2 * i) + 1
                op = rest[idx]
                if op in valid_ops:
                    rest = (
                        rest[: idx - 1]
                        + [Calculator.OPS[op](rest[idx - 1], rest[idx + 1])]
                        + rest[idx + 2 :]
                    )
                else:
                    i += 1

        if len(rest) != 1:
            print(rest)
            raise Exception("failed to reduce equation")

        return rest[0]

    def run(self):
        return self.parse_expr(self.data)


def part1(data):
    return sum([Calculator(line).run() for line in data])


def part2(data):
    return sum([Calculator(line, 2).run() for line in data])


print("part1:", part1(data))
print("part2:", part2(data))
