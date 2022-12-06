from adventlib import AOC, window


def num_until_unique_window(data, n):
    for (i, data) in enumerate(window(data, n), n):
        if len(set(data)) == n:
            return i
    return None


class Day6(AOC):
    def process_input(self, raw_data):
        return list(raw_data.strip())

    def part1(self):
        return num_until_unique_window(self.data, 4)

    def part2(self):
        return num_until_unique_window(self.data, 14)


if __name__ == "__main__":
    aoc = Day6()
    aoc.run()
