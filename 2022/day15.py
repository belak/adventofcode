from adventlib import AOC


def manhattan(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def visible(data, pt):
    for (sensor, _, max_dist) in data:
        if manhattan(sensor, pt) <= max_dist:
            return True
    return False


class Day15(AOC):
    def process_input(self, raw_data: str):
        data = []
        for line in raw_data.splitlines():
            line = line.removeprefix("Sensor at x=").split(": closest beacon is at x=")
            pt1 = tuple(map(int, line[0].split(", y=")))
            pt2 = tuple(map(int, line[1].split(", y=")))

            data.append((pt1, pt2, manhattan(pt1, pt2)))
        return data

    def part1(self):
        # Find reasonable start/end points
        min_x = min([line[0][0] - line[2] for line in self.data])
        max_x = max([line[0][0] + line[2] for line in self.data])

        # Build a set of beacons we already know about
        beacons = set([line[1] for line in self.data])

        # Loop through the reasonable start/end points we found. If it's visible
        # by at least one sensor and isn't a beacon we know about, add it to our
        # total.
        total = 0
        for x in range(min_x, max_x + 1):
            pt = (x, 2000000)
            if pt in beacons:
                continue
            if visible(self.data, pt):
                total += 1

        return total

    def part2(self):
        for (sensor, _, max_dist) in self.data:
            # Generating all points by generating a quadrant of points and
            # miltiplying multiplying them by factors to get the other
            # quadrants.

            # We can generate all dx and dy values by generating one of them
            # (from 0 to max_dist + 1) and then subtracting it from the
            # manhattan distance (plus one).
            for dx in range(max_dist + 2):  # [0, max_dist + 1]
                dy = (max_dist + 1) - dx

                # Each of these x factors and y factors puts dx and dy in a
                # different quadrant. Because the pattern from the sensor is a
                # diamond, it's symmetrical and this works.
                for xfact, yfact in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    pt = (sensor[0] + (dx * xfact), sensor[1] + (dy * yfact))

                    # Constraints provided
                    if not (0 <= pt[0] <= 4000000 and 0 <= pt[1] <= 4000000):
                        continue

                    # If no sensors could see it, we found our point!
                    if not visible(self.data, pt):
                        print(pt)
                        return (pt[0] * 4000000) + pt[1]


if __name__ == "__main__":
    aoc = Day15()
    aoc.run()
