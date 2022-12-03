from adventlib import AOC, split_chunks


def item_val(item):
    if item.isupper():
        return ord(item) - ord("A") + 27
    else:
        return ord(item) - ord("a") + 1


class Day3(AOC):
    def part1(self):
        total = 0
        for line in self.data:
            c1_items = set(line[: len(line) // 2])
            c2_items = set(line[len(line) // 2 :])
            for item in c1_items.intersection(c2_items):
                total += item_val(item)

        return total

    def part2(self):
        total = 0
        for group in split_chunks(self.data, 3):
            r1 = set(group[0])
            r2 = set(group[1])
            r3 = set(group[2])

            badge_items = r1.intersection(r2, r3)
            for item in badge_items:
                total += item_val(item)

        return total


if __name__ == "__main__":
    aoc = Day3()
    aoc.run()
