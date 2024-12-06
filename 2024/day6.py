data = [list(line.strip()) for line in open("./input-6").readlines()]


DIRS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


def find_starting_pos(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "^":
                return (x, y)


def print_grid(data, pos):
    pos_x, pos_y = pos
    for y in range(len(data)):
        for x in range(len(data[y])):
            if pos_x == x and pos_y == y:
                print("X", end="")
            else:
                print(data[y][x], end="")
        print()


(start_x, start_y) = find_starting_pos(data)
data[start_y][start_x] = "."


def patrol(data, x, y):
    current_dir_index = 0

    visited = set()
    visited.add((x, y))

    visited_with_dirs = set()

    while True:
        (dx, dy) = DIRS[current_dir_index % 4]

        new_x = x + dx
        new_y = y + dy

        if not (0 <= new_y < len(data) and 0 <= new_x < len(data[new_y])):
            return visited

        next_tile = data[y + dy][x + dx]
        if next_tile == "#":
            current_dir_index += 1
        elif next_tile == ".":
            x += dx
            y += dy
            visited.add((x, y))

            target = (x, y, dx, dy)
            if target in visited_with_dirs:
                return None
            visited_with_dirs.add(target)


print(len(patrol(data, start_x, start_y)))

total = 0
for y in range(len(data)):
    for x in range(len(data[1])):
        if x == start_x and y == start_y:
            continue
        if data[y][x] == "#":
            continue

        data[y][x] = "#"

        if patrol(data, start_x, start_y) is None:
            total += 1

        data[y][x] = "."

print(total)
