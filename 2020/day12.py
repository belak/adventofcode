from math import sin, cos, radians

lines = [(line[0], int(line[1:])) for line in open("day12-input").read().splitlines()]


DIRS = ["N", "E", "S", "W"]


class State:
    def __init__(self, data):
        self.data = data
        self.dir = 1
        self.pos = (0, 0)

    def run(self):
        for item in self.data:
            direction = item[0]
            magnitude = item[1]
            facing = DIRS[self.dir]

            if direction == "N" or (direction == "F" and facing == "N"):
                self.pos = (self.pos[0], self.pos[1] + magnitude)
            elif direction == "S" or (direction == "F" and facing == "S"):
                self.pos = (self.pos[0], self.pos[1] - magnitude)
            elif direction == "E" or (direction == "F" and facing == "E"):
                self.pos = (self.pos[0] + magnitude, self.pos[1])
            elif direction == "W" or (direction == "F" and facing == "W"):
                self.pos = (self.pos[0] - magnitude, self.pos[1])
            elif direction == "L":
                self.dir = (self.dir - (magnitude // 90)) % 4
                self.dir += 4
                self.dir = self.dir % 4
            elif direction == "R":
                self.dir = (self.dir + (magnitude // 90)) % 4
            elif direction == "F":
                raise Exception("unknown facing direction")
            else:
                raise Exception("unknown direction")

        return self.pos

    def run2(self):
        self.pos = (10, 1)

        ship = (0, 0)

        for item in self.data:
            direction = item[0]
            magnitude = item[1]

            if direction == "N":
                self.pos = (self.pos[0], self.pos[1] + magnitude)
            elif direction == "S":
                self.pos = (self.pos[0], self.pos[1] - magnitude)
            elif direction == "E":
                self.pos = (self.pos[0] + magnitude, self.pos[1])
            elif direction == "W":
                self.pos = (self.pos[0] - magnitude, self.pos[1])
            elif direction == "L":
                rotate_count = 4 - (magnitude // 90)
                for i in range(rotate_count):
                    self.pos = (
                        self.pos[1],
                        -1 * self.pos[0],
                    )
            elif direction == "R":
                rotate_count = magnitude // 90
                for i in range(rotate_count):
                    self.pos = (
                        self.pos[1],
                        -1 * self.pos[0],
                    )
            elif direction == "F":
                ship = (
                    ship[0] + (self.pos[0] * magnitude),
                    ship[1] + (self.pos[1] * magnitude),
                )
            else:
                raise Exception("unknown direction")

        return ship


def part1(data):
    state = State(data)
    ret = state.run()
    return abs(ret[0]) + abs(ret[1])


def part2(data):
    state = State(data)
    ret = state.run2()
    return abs(ret[0]) + abs(ret[1])


print("part1:", part1(lines))
print("part2:", part2(lines))
