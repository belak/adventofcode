from adventlib import AOC, straight_line_points, print_map

from collections import defaultdict


SAND_DIRS = [(0, -1), (-1, -1), (1, -1)]


def step(data, point):
    for (dx, dy) in SAND_DIRS:
        if data[(point[0] + dx, point[1] + dy)] == ".":
            return (point[0] + dx, point[1] + dy)
    return None


class Day14(AOC):
    def process_input(self, raw_data):
        lines = [
            list(map(lambda x: tuple(map(int, x.split(","))), line.split(" -> ")))
            for line in raw_data.splitlines()
        ]
        data = defaultdict(lambda: ".")
        for line in lines:
            prev = line[0]
            for end in line[1:]:
                for (x, y) in straight_line_points(prev, end):
                    # Note that we invert the Y value to make printing the grid
                    # make more sense, and to make gravity cause the number to
                    # go down which my brain finds easier to reason about.
                    data[(x, -y)] = "#"
                prev = end
        return data

    def part1(self):
        min_y = min(map(lambda pt: pt[1], self.data.keys()))

        count = 0
        while True:
            loc = (500, 0)
            while next_loc := step(self.data, loc):
                # The first particle to make it past the min_y value stops the
                # simulation.
                if next_loc[1] <= min_y:
                    return count

                loc = next_loc

            count += 1
            self.data[loc] = "o"

    def part2(self):
        min_x = min(map(lambda pt: pt[0], self.data.keys()))
        max_x = max(map(lambda pt: pt[0], self.data.keys()))
        min_y = min(map(lambda pt: pt[1], self.data.keys()))

        # Draw an extra really long line 2 units "below" the floor. It won't
        # work for every case, but it's good enough for AoC.
        for (x, y) in straight_line_points(
            (min_x - 1000, min_y - 2), (max_x + 1000, min_y - 2)
        ):
            self.data[(x, y)] = "#"

        count = 0
        while True:
            loc = (500, 0)
            while next_loc := step(self.data, loc):
                loc = next_loc

            count += 1
            self.data[loc] = "o"

            # If we finished an iteration and the particle hasn't moved, stop
            # the simulation.
            if loc == (500, 0):
                return count


if __name__ == "__main__":
    aoc = Day14()
    aoc.run()
