from math import isqrt
import numpy as np

tiles = [
    section.splitlines()
    for section in open("day20-input").read().split("\n\n")
    if section.strip() != ""
]


def flipped_candidates(tile):
    return [
        np.flip(tile, axis=0),
        np.flip(tile, axis=1),
        np.flip(tile, axis=(0, 1)),
    ]


def rotated_candidates(tile):
    return [
        np.rot90(tile, k=1),
        np.rot90(tile, k=2),
        np.rot90(tile, k=3),
    ]


def all_candidates(tile):
    tmp = [np.array(tile)]
    tmp += rotated_candidates(tile)

    ret = []
    for arr in tmp:
        ret += [arr]
        ret += flipped_candidates(arr)

    return ret


tiles = {
    int(tile[0][5:-1]): all_candidates(list(map(list, tile[1:]))) for tile in tiles
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


def assemble(final_map, available_tiles, counter, size):
    if len(available_tiles) == 0:
        return final_map

    x = counter % size
    y = counter // size

    print(counter, x, y)

    north_tile = None
    if x != 0:
        north_tile_id = final_map[(x - 1, y)]
        north_tile = tiles[north_tile_id[0]][north_tile_id[1]]

    west_tile = None
    if y != 0:
        west_tile_id = final_map[(x, y - 1)]
        west_tile = tiles[west_tile_id[0]][west_tile_id[1]]

    for tile_id in available_tiles:
        for offset, tile in enumerate(tiles[tile_id]):
            if north_tile is not None and bottom(north_tile) != top(tile):
                continue

            if west_tile is not None and right(west_tile) != left(tile):
                continue

            final_map[(x, y)] = (tile_id, offset)

            ret = assemble(
                final_map,
                list(filter(lambda x: x != tile_id, available_tiles)),
                counter + 1,
                size,
            )
            if ret is not None:
                return ret

            del final_map[(x, y)]

    return None


def part1(tiles):
    grid_size = isqrt(len(tiles))
    final_map = assemble({}, tiles.keys(), 0, grid_size)

    print(final_map)

    return (
        int(final_map[(0, 0)][0])
        * int(final_map[(0, grid_size - 1)][0])
        * int(final_map[(grid_size - 1, 0)][0])
        * int(final_map[(grid_size - 1, grid_size - 1)][0])
    )


def part2(data):
    return -1


print("part1:", part1(tiles))
print("part2:", part2(tiles))
