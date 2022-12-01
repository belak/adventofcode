from adventlib import AOC

import numpy

bin_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

class Packet:
    version = None
    type_id = None
    len_type_id = None
    val = None
    children = None
    extra = ""

    def __init__(self, data):
        self.children = []

        self.version = int(data[0:3], 2)
        self.type_id = int(data[3:6], 2)

        rest = data[6:]

        if self.type_id == 4:
            chunk_data = ""
            while True:
                kind = rest[0]
                chunk_data += rest[1:5]
                rest = rest[5:]
                if kind == '0':
                    break

            self.val = int(chunk_data, 2)
        else:
            self.len_type_id = int(rest[0:1], 2)
            rest = rest[1:]

            if self.len_type_id == 0:
                size = int(rest[0:15], 2)
                rest = rest[15:]
                inner_rest = rest[:size]
                rest = rest[size:]

                while inner_rest:
                    inner = Packet(inner_rest)
                    self.children.append(inner)
                    inner_rest = inner.extra


            elif self.len_type_id == 1:
                sub_packets = int(rest[0:11], 2)
                rest = rest[11:]

                for _ in range(sub_packets):
                    inner = Packet(rest)
                    self.children.append(inner)
                    rest = inner.extra
            else:
                raise Exception("unknown len_type_id: {}".format(self.len_type_id))

        self.extra = rest

    def calculate(self):
        if self.type_id == 4:
            return self.val

        child_values = [p.calculate() for p in self.children]
        if self.type_id == 0:
            return sum(child_values)
        elif self.type_id == 1:
            return numpy.prod(child_values)
        elif self.type_id == 2:
            return min(child_values)
        elif self.type_id == 3:
            return max(child_values)
        elif self.type_id == 5:
            return 1 if child_values[0] > child_values[1] else 0
        elif self.type_id == 6:
            return 1 if child_values[0] < child_values[1] else 0
        elif self.type_id == 7:
            return 1 if child_values[0] == child_values[1] else 0
        else:
            raise Exception("unknown type_id: {}".format(self.type_id))

    def __str__(self):
        return "Packet<{}, {}, {}, [{}]>".format(self.version, self.type_id, self.val, ','.join(map(str, self.children)))


class Day16(AOC):
    def process_input(self, raw_data):
        return ''.join(map(lambda x: bin_map[x], raw_data.strip()))

    def part1(self):
        v = 0

        packets = [Packet(self.data)]

        while packets:
            p = packets.pop()
            v += p.version
            packets.extend(p.children)

        return v

    def part2(self):
        return Packet(self.data).calculate()


if __name__ == '__main__':
    aoc = Day16()
    aoc.run()
