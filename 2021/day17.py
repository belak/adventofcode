from adventlib import AOC


def hits_target(x_range, y_range, dx, dy):
    x = 0
    y = 0

    max_y = 0

    while True:
        if x > x_range[1]:
            return False

        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            return max_y

        if dx == 0 and y < y_range[0]:
            return False

        x += dx
        y += dy

        if y > max_y:
            max_y = y

        if dx > 0:
            dx -= 1

        dy -= 1


class Day17(AOC):
    def process_input(self, raw_data):
        raw_data = raw_data.removeprefix("target area: ")
        (x, y) = raw_data.split(", ")
        self.x_range = tuple(map(int, x[2:].split("..")))
        self.y_range = tuple(map(int, y[2:].split("..")))

    def part1(self):
        ret = -10000
        for dx in range(0, self.x_range[1]):
            for dy in range(self.y_range[0], 200):
                max_y = hits_target(self.x_range, self.y_range, dx, dy)
                if max_y > ret:
                    ret = max_y
        return ret


    def part2(self):
        ret = 0
        for dx in range(0, self.x_range[1]+(self.x_range[1]-self.x_range[0])):
            for dy in range(self.y_range[0], 200):
                max_y = hits_target(self.x_range, self.y_range, dx, dy)
                if max_y is not False:
                    ret += 1
        return ret


if __name__ == "__main__":
    aoc = Day17()
    aoc.run()
