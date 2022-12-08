from adventlib import AOC, parse_2d_grid

from numpy import flip


class Day8(AOC):
    def process_input(self, raw_data):
        return parse_2d_grid(raw_data)

    def part1(self):
        total = 0

        for x in range(len(self.data)):
            for y in range(len(self.data[0])):
                left = flip(self.data[x, :y])
                right = self.data[x, y + 1 :]
                up = flip(self.data[:x, y])
                down = self.data[x + 1 :, y]

                if any(
                    [
                        all(map(lambda i: i < self.data[x, y], left)),
                        all(map(lambda i: i < self.data[x, y], right)),
                        all(map(lambda i: i < self.data[x, y], up)),
                        all(map(lambda i: i < self.data[x, y], down)),
                    ]
                ):
                    total += 1

        return total

    def part2(self):
        total = 0

        for x in range(len(self.data)):
            for y in range(len(self.data[0])):
                left = flip(self.data[x, :y])
                right = self.data[x, y + 1 :]
                up = flip(self.data[:x, y])
                down = self.data[x + 1 :, y]

                def first_idx(arr, target, default):
                    for (i, val) in enumerate(arr):
                        if val >= target:
                            return i + 1
                    return default

                l = first_idx(left, self.data[x, y], len(left))
                r = first_idx(right, self.data[x, y], len(right))
                u = first_idx(up, self.data[x, y], len(up))
                d = first_idx(down, self.data[x, y], len(down))

                if u * r * d * l > total:
                    total = u * r * d * l

        return total


if __name__ == "__main__":
    aoc = Day8()
    aoc.run()
