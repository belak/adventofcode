from collections import namedtuple, defaultdict
from copy import copy

data = open("day17-input").read().splitlines()

ACTIVE = '#'
INACTIVE = '.'


Point = namedtuple('Point', ['x', 'y', 'z'])

offsets = []
for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            if i == j == k == 0:
                continue

            offsets += [Point(i, j, k)]


class State:
    def __init__(self, initial_state):
        self.gen = 0
        self.state = defaultdict(lambda: INACTIVE)
        self.min = Point(0, 0, 0)
        self.max = Point(0, 0, 0)

        for y, line in enumerate(initial_state):
            for x, val in enumerate(line):
                pos = Point(x, y, 0)
                self.update_max(x=x, y=y)
                self.state[pos] = val

    def update_max(self, x=None, y=None, z=None):
        if x is None or x < self.max.x:
            x = self.max.x
        if y is None or y < self.max.y:
            y = self.max.y
        if z is None or z < self.max.z:
            z = self.max.z

        self.max = Point(x, y, z)

    def update_min(self, x=None, y=None, z=None):
        if x is None or x > self.min.x:
            x = self.min.x
        if y is None or y > self.min.y:
            y = self.min.y
        if z is None or z > self.min.z:
            z = self.min.z

        self.min = Point(x, y, z)

    def step(self):
        self.gen += 1
        print(f'step gen {self.gen}')

        prev_state = copy(self.state)

        for z in range(self.min[2] - 1, self.max[2] + 2):
            for y in range(self.min[1] - 1, self.max[1] + 2):
                for x in range(self.min[0] - 1, self.max[0] + 2):
                    num_alive = 0
                    for offset in offsets:
                        pos = Point(x + offset.x, y + offset.y, z + offset.z)
                        if prev_state[pos] == ACTIVE:
                            num_alive += 1
                    cur = Point(x, y, z)
                    if prev_state[cur] == ACTIVE:
                        if num_alive != 2 and num_alive != 3:
                            self.state[cur] = INACTIVE
                    elif prev_state[cur] == INACTIVE:
                        if num_alive == 3:
                            self.state[cur] = ACTIVE
                            self.update_max(cur.x, cur.y, cur.z)
                            self.update_min(cur.x, cur.y, cur.z)


    def dump(self):
        print(f"gen={self.gen}")
        for z in range(self.min[2], self.max[2] + 1):
            print(f"z={z}")
            for y in range(self.min[1], self.max[1] + 1):
                for x in range(self.min[0], self.max[0] + 1):
                    pos = Point(x, y, z)
                    print(self.state[pos], end='')
                print()
            print()

    def count_active(self):
        total = 0
        for item in self.state.values():
            if item == ACTIVE:
                total += 1
        return total



def part1(initial_state):
    state = State(initial_state)
    for i in range(6):
        state.step()
    return state.count_active()


print('part1:', part1(data))
