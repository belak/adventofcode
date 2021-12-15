from adventlib import CARDINAL_DIRS as dirs, load_2d_grid

data = load_2d_grid("day9-input")

tmp = {}
for y in range(len(data)):
    for x in range(len(data[y])):
        tmp[(x, y)] = data[y][x]
data = tmp

low_sum = 0
low_points = []

for pt, val in data.items():
    ok = True

    for dx, dy in dirs:
        d_pt = (pt[0] + dx, pt[1] + dy)
        if d_pt in data and data[d_pt] <= val:
            ok = False
            break

    if ok:
        low_sum += val + 1
        low_points.append(pt)

print(low_sum)

basins = []

# Simple bfs to visit all nodes and create basins out of them.
for low_pt in low_points:
    visited = set()
    queue = [low_pt]
    while queue:
        pt = queue.pop(0)
        for dx, dy in dirs:
            next_pt = (pt[0] + dx, pt[1] + dy)
            if next_pt not in data or next_pt in visited or data[next_pt] == 9:
                continue

            visited.add(next_pt)
            queue.append(next_pt)
    basins.append(len(visited))

basins = sorted(basins, reverse=True)

print(basins[0] * basins[1] * basins[2])
