import numpy as np

from adventlib import ORDINAL_DIRS as dirs, load_2d_grid

data = load_2d_grid("day11-input")

count = 0

i = 0
while True:
    # This feels like cheating, thanks numpy
    data += 1

    flashed = set()

    items = np.where(data > 9)
    items = set(zip(items[0], items[1]))
    while len(items - flashed) > 0:
        for coord in items:
            if coord in flashed:
                continue

            flashed.add(coord)

            for dx, dy in dirs:
                new_x = coord[1] + dx
                new_y = coord[0] + dy

                if new_x < 0 or new_y < 0:
                    continue

                try:
                    data[new_y, new_x] += 1
                except Exception as e:
                    pass

        items = np.where(data > 9)
        items = set(zip(items[0], items[1]))

    for item in flashed:
        data[item[0], item[1]] = 0

    if i < 100:
        count += len(flashed)
    else:
        if np.all(data == 0):
            break

    i += 1


print(count)
print(i + 1)
