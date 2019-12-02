calc = {}

class Circuit:
    def __init__(self, filename, overrides=None):
        self.ops = {
            'AND': Circuit.and_op,
            'OR': Circuit.or_op,
            'NOT': Circuit.not_op,
            'RSHIFT': Circuit.rshift_op,
            'LSHIFT': Circuit.lshift_op,
        }

        self.input = {}
        self.results = {}
        for line in open('input/day7'):
            ops, res = line.strip().split(' -> ')
            self.input[res] = ops.split(' ')

        if overrides is not None:
            for k, v in overrides.items():
                self.input[k] = v

    def not_op(val):
        return ~val

    def and_op(val1, val2):
        return val1 & val2

    def or_op(val1, val2):
        return val1 | val2

    def rshift_op(val1, val2):
        return val1 >> val2

    def lshift_op(val1, val2):
        return val1 << val2

    def value(self, name):
        # This is a dirty hack to attempt parsing as an int
        try:
            return int(name)
        except ValueError:
            pass

        ops = self.input[name]
        if name not in self.results:
            if len(ops) == 1:
                res = self.value(ops[0])
            else:
                op = ops[-2]
                if op == 'NOT':
                    res = Circuit.not_op(self.value(ops[1]))
                else:
                    res = self.ops[op](self.value(ops[0]), self.value(ops[2]))

            self.results[name] = res

        return self.results[name]

c = Circuit('input/day7')
print(c.value('a'))

c = Circuit('input/day7', {'b': [c.value('a')]})
print(c.value('a'))
