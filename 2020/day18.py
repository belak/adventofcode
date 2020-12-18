# NOTE: most days we don't massage the data like this, but I didn't want to deal
# with parsing out open/close parens inside existing items. By adding spaces, we
# can handle them exactly the same as normal tokens.
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

        # A value can only be either an open paren or a value.
        if item == "(":
            # For open paren, we split the expression into 2 pieces: the portion
            # inside the parens, and what comes after.
            expr, rest = self.split_inner_expr(rest)

            # Now that it's split, we recurse and try to handle the expression
            # that was inside these parens. Because we properly reduce it to a
            # value, we're still returning a single value here (followed by the
            # rest of the equation).
            return self.parse_expr(expr), rest
        else:
            return int(item), rest

    def split_inner_expr(self, line):
        # This takes the remainder of a line right after an open paren and
        # splits it into the portion inside the parens (handling nested parens
        # properly), and what comes after the parenthetical expression.
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
        # Start by flattening out this array - calculate any nested parens as a
        # value. This will leave us with an array in the form of [value, op,
        # value, ..., op, value]. We can take the array in that form and reduce
        # it by running passes on it for each stage of operators.
        total, rest = self.parse_value(data)
        tmp = [total]
        while len(rest) > 0:
            arg, rest = rest[0], rest[1:]
            val, rest = self.parse_value(rest)
            tmp += [arg, val]
        rest = tmp

        # For mode 1, all operations are the same level, while for mode 2,
        # they're separate and in a specific order.
        if self.mode == 1:
            precidence = ["+*"]
        else:
            precidence = ["+", "*"]

        # Essentially, do a pass for each op set (in order of precidence) to
        # reduce the array. When we get to the end, we should have 1 element
        # in the list.
        for valid_ops in precidence:
            # We want to loop through the operators and make decisions based on
            # those.
            i = 1
            while i < len(rest):
                op = rest[i]
                if op in valid_ops:
                    # For every valid op, we split the values into 3 parts:
                    #
                    # - What came before this operation
                    # - The set of 3 items which make up an operation (value, op, value)
                    # - What comes after this operation

                    prev = rest[: i - 1]
                    calc = Calculator.OPS[op](rest[i - 1], rest[i + 1])
                    post = rest[i + 2 :]

                    rest = prev + [calc] + post
                else:
                    # If this wasn't a valid op for this phase, move on to the
                    # next value.
                    i += 2

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
