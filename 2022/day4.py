from adventlib import AOC


class Day4(AOC):
    def process_input(self, raw_data):
        ret = []
        for line in raw_data.strip().splitlines():
            data = line.split(',')
            elf1 = data[0].split('-')
            elf2 = data[1].split('-')
            ret.append((
                (int(elf1[0]), int(elf1[1])),
                (int(elf2[0]), int(elf2[1])),
            ))
        return ret

    def part1(self):
        total = 0
        for line in self.data:
            elf1 = line[0]
            elf2 = line[1]
            if elf1[0] <= elf2[0] and elf1[1] >= elf2[1]:
                total += 1
            elif elf2[0] <= elf1[0] and elf2[1] >= elf1[1]:
                total += 1

        return total

    def part2(self):
        total = 0
        for line in self.data:
            elf1 = line[0]
            elf2 = line[1]
            if elf1[0] <= elf2[0] and elf1[1] >= elf2[0]:
                total += 1
            elif elf1[1] >= elf2[1] and elf1[0] <= elf2[1]:
                total += 1
            elif elf2[0] <= elf1[0] and elf2[1] >= elf1[0]:
                total += 1
            elif elf2[1] >= elf1[1] and elf2[0] <= elf1[1]:
                total += 1

        return total


if __name__ == "__main__":
    aoc = Day4()
    aoc.run()
