from collections import defaultdict

from adventlib import AOC


DIRECTIONS = {
     "U": (0, 1),
     "R": (1, 0),
     "D": (0, -1),
     "L": (-1, 0),
}


def move_tail(head, tail):
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return tail

    dx = 0
    dy = 0

    if head[0] > tail[0]:
        dx = 1
    elif head[0] < tail[0]:
        dx = -1

    if head[1] > tail[1]:
        dy = 1
    elif head[1] < tail[1]:
        dy = -1

    return (tail[0] + dx, tail[1] + dy)


class Day9(AOC):
    def process_input(self, raw_data):
        return [tuple(line.split(" ")) for line in raw_data.splitlines()]

    def part1(self):
        grid = defaultdict(lambda: ".")
        prev_head = head = (0, 0)
        tail = (0, 0)

        # Mark the starting point as visited
        grid[(0, 0)] = "#"

        for (d, amount) in self.data:
            amount = int(amount)
            (dx, dy) = DIRECTIONS[d]

            for i in range(1, amount + 1):
                head = (prev_head[0] + dx * i, prev_head[1] + dy * i)
                tail = move_tail(head, tail)
                grid[tail] = "#"

            prev_head = head

        return len(list(filter(lambda x: x == "#", grid.values())))

    def part2(self):
        grid = defaultdict(lambda: ".")
        prev_head = head = (0, 0)

        # Make a tail of 9 elements - the head plus the 9 makes 10.
        tail = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        # Mark the starting point as visited
        grid[(0, 0)] = "#"

        for (d, amount) in self.data:
            amount = int(amount)
            (dx, dy) = DIRECTIONS[d]

            for i in range(1, amount + 1):
                head = target = (prev_head[0] + dx * i, prev_head[1] + dy * i)
                for j in range(len(tail)):
                    tail[j] = target = move_tail(target, tail[j])

                # After looping through everything, target will contain the
                # actual tail node, so we mark that as visited.
                grid[target] = "#"

            prev_head = head

        return len(list(filter(lambda x: x == "#", grid.values())))


if __name__ == "__main__":
    aoc = Day9()
    aoc.run()
