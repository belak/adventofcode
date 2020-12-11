from copy import copy
from collections import defaultdict

offsets = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (0, -1),
]

lines = open("day11-input").read().splitlines()

data = {}
for i in range(len(lines)):
    for j in range(len(lines[i])):
        data[(i, j)] = lines[i][j]


max_coord = (0, 0)
for key in data.keys():
    if key[0] > max_coord[0] or key[1] > max_coord[1]:
        max_coord = key

part2_offsets = {}
for key in data.keys():
    for offset in offsets:
        for i in range(1, max(max_coord)+1):
            coord = (key[0] + i * offset[0], key[1] + i * offset[1])
            seat = data.get(coord, '')

            if seat == '':
                break

            if seat == '#' or seat == 'L':
                part2_offsets[(key, offset)] = coord
                break


class State:
    def __init__(self, data):
        self.gen = 0
        self.prev = data.copy()
        self.cur = data.copy()

    def _step(self, offset_coord, occupied_threshold):
        self.gen += 1

        changed = False

        self.prev = self.cur.copy()

        for key in self.prev.keys():
            occupied = 0
            for offset in offsets:
                coord = offset_coord(key, offset)
                if coord is None:
                    continue

                if self.prev.get(coord, '') == '#':
                    occupied += 1

            cur_seat = self.cur.get(key, '')
            if cur_seat == '#':
                if occupied >= occupied_threshold:
                    self.cur[key] = 'L'
                    changed = True
            elif cur_seat == 'L':
                if occupied == 0:
                    self.cur[key] = '#'
                    changed = True
            elif cur_seat == '.':
                pass
            else:
                raise Exception(f'unknown value: {cur_seat}')

        return changed

    def step1(self):
        # Step 1, we always look at the seats right around us
        def offset_coord(key, offset):
            return (key[0] + offset[0], key[1] + offset[1])

        return self._step(offset_coord, 4)

    def step2(self):
        def offset_coord(key, offset):
            return part2_offsets.get((key, offset))

        return self._step(offset_coord, 5)

    def print(self):
        print(max_coord)
        for j in range(max_coord[0]+1):
            for i in range(max_coord[1]+1):
                print(self.cur[(j, i)], end='')
            print()

    def occupied(self):
        occupied = 0
        for val in self.cur.values():
            if val == '#':
                occupied += 1

        return occupied


def part1(data):
    state = State(data)

    while state.step1():
        pass

    return (state.gen, state.occupied())


def part2(data):
    state = State(data)

    while state.step2():
       pass

    return (state.gen, state.occupied())


print('part1:', part1(data))
print('part2:', part2(data))
