from collections import defaultdict
from math import isqrt
import numpy as np

from aoc import print_grid


NESSIE = """\
                  #
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()
NESSIE_HASHES = 15


tiles = [
    section.splitlines()
    for section in open("day20-input").read().split("\n\n")
    if section.strip() != ""
]


tiles = {
    int(tile[0][5:-1]): np.array(list(map(list, tile[1:]))) for tile in tiles
}

# Utils
def top(tile):
    return "".join(tile[0])


def bottom(tile):
    return "".join(tile[-1])


def left(tile):
    return "".join([x[0] for x in tile])


def right(tile):
    return "".join([x[-1] for x in tile])


def possible_orientations(tile):
    for _ in range(4):
        yield tile
        yield np.flip(tile, axis=0)
        tile = np.rot90(tile)


def build_map(tiles):
    grid_size = isqrt(len(tiles))

    edge_map = defaultdict(set)
    for tile_id, tile in tiles.items():
        edge_map[top(tile)].add(tile_id)
        edge_map[bottom(tile)].add(tile_id)
        edge_map[left(tile)].add(tile_id)
        edge_map[right(tile)].add(tile_id)

        # We need to add all the reversed edges as well because they're valid sides for flipped/rotated tiles.
        edge_map[top(tile)[::-1]].add(tile_id)
        edge_map[bottom(tile)[::-1]].add(tile_id)
        edge_map[left(tile)[::-1]].add(tile_id)
        edge_map[right(tile)[::-1]].add(tile_id)

    # Count how many neighbors each tile has - it seems like all the tiles can only go in one location, so this is the simplest option.
    neighbor_count = {}
    for tile_id, tile in tiles.items():
        total = len(edge_map[top(tile)]) - 1
        total += len(edge_map[bottom(tile)]) - 1
        total += len(edge_map[left(tile)]) - 1
        total += len(edge_map[right(tile)]) - 1

        if total < 2 or total > 4:
            raise Exception(f'tile has invalid number of neighbors: {total}')

        neighbor_count[tile_id] = total    

    corners = [tile_id for tile_id, count in neighbor_count.items() if count == 2]
    #edges = [tile_id for tile_id, count in neighbor_count.items() if count == 3]
    #middles = [tile_id for tile_id, count in neighbor_count.items() if count == 4]

    final_map = {}
    
    # Pick a corner to start with and ensure it's rotated correctly.
    start_id = corners[0]
    start_tile = tiles[start_id]
    while len(edge_map[top(start_tile)]) > 1 or len(edge_map[left(start_tile)]) > 1:
        start_tile = np.rot90(start_tile)
    final_map[(0, 0)] = (start_id, start_tile)

    # Fill in the top based on the tiles to the left of the current tile.
    for y in range(1, grid_size):
        prev_title_id, prev_tile = final_map[(0, y-1)]

        next_tile_id = next(iter(edge_map[right(prev_tile)] - set([prev_title_id])))
        for tile in possible_orientations(tiles[next_tile_id]):
            if left(tile) == right(prev_tile):
                final_map[(0, y)] = (next_tile_id, tile)
                break

    # Fill in each column the same way, but searching based on the tile above rather than to the side.
    for x in range(1, grid_size):
        for y in range(0, grid_size):
            prev_title_id, prev_tile = final_map[(x-1, y)]

            next_tile_id = next(iter(edge_map[bottom(prev_tile)] - set([prev_title_id])))
            for tile in possible_orientations(tiles[next_tile_id]):
                if top(tile) == bottom(prev_tile):
                    final_map[(x, y)] = (next_tile_id, tile)
                    break

    return final_map


def part1(tiles):
    grid_size = isqrt(len(tiles))
    final_map = build_map(tiles)

    return (
        int(final_map[(0, 0)][0])
        * int(final_map[(0, grid_size - 1)][0])
        * int(final_map[(grid_size - 1, 0)][0])
        * int(final_map[(grid_size - 1, grid_size - 1)][0])
    )


def check_nessie(grid, x, y):
    for x1 in range(len(NESSIE)):
        for y1 in range(len(NESSIE[0])):
            if NESSIE[x1][y1] != '#':
                continue
            if grid[x+x1][y+y1] != '#':
                return False
    return True

def part2(data):
    grid_size = isqrt(len(tiles))
    final_map = build_map(tiles)

    output_tile_size = len(final_map[(0, 0)][1]) - 2
    rows = cols = grid_size * output_tile_size
    
    blank_row = [' ' for _ in range(cols)]
    grid = np.array([blank_row.copy() for _ in range(rows)])

    total_hashes = 0
    for raw_x in range(grid_size):
        x = output_tile_size * raw_x
        for raw_y in range(grid_size):
            y = output_tile_size * raw_y
            tile = final_map[(raw_x, raw_y)][1]

            for x1, tile_row in enumerate(tile[1:-1]):
                for y1, val in enumerate(tile_row[1:-1]):
                    grid[x+x1][y+y1] = val

                    if val == '#':
                        total_hashes += 1

    #print_grid(grid)

    for pic in possible_orientations(grid):
        total = 0
        for x in range(len(pic) - len(NESSIE)):
            for y in range(len(pic[x]) - len(NESSIE[0])):
                if check_nessie(pic, x, y):
                    total += 1

        if total:
            return total_hashes - (total * NESSIE_HASHES)

    return -1


print("part1:", part1(tiles))
print("part2:", part2(tiles))
