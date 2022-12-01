from adventlib import AOC

class Day1(AOC):
    def process_input(self, raw_data):
        elves = raw_data.split('\n\n')
        elves = [[int(line) for line in elf.strip().split('\n')] for elf in elves]
        return elves

    def part1(self):
        return max(map(lambda elf: sum(elf), self.data))

    def part2(self):
        vals = list(sorted(map(lambda elf: sum(elf), self.data)))
        return vals[-1] + vals[-2] + vals[-3]


if __name__ == '__main__':
    aoc = Day1()
    aoc.run()
