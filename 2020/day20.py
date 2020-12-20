from collections import defaultdict
from math import isqrt

tiles = [
    section.splitlines()
    for section in open("day20-input").read().split("\n\n")
    if section.strip() != ""
]

# Utils
def top(tile):
    return "".join(tile[0])


def bottom(tile):
    return "".join(tile[-1])


def left(tile):
    return "".join([x[0] for x in tile])


def right(tile):
    return "".join([x[-1] for x in tile])


# Candidate generation
def rotated_candidates(tile):
    candidates = []
    last = tile
    for _ in range(3):
        tile = [line[:] for line in tile]
        for x in range(len(tile)):
            for y in range(len(tile[x])):
                tile[x][y] = last[len(tile[x]) - y - 1][x]
        last = tile
        candidates.append(tile)
    return candidates


def flipped_candidates(tile):
    candidates = []
    candidates.append(tile[::-1])
    candidates.append([line[::-1] for line in tile])
    candidates.append([line[::-1] for line in tile][::-1])
    return candidates


def all_candidates(tile):
    candidates = [tile]
    for candidate in rotated_candidates(tile):
        candidates.append(candidate)

    for candidate in flipped_candidates(tile):
        candidates.append(candidate)
        for inner_candidate in rotated_candidates(candidate):
            candidates.append(inner_candidate)

    return candidates


tiles = {
    int(tile[0][5:-1]): all_candidates(list(map(list, tile[1:]))) for tile in tiles
}


south_adjacency = defaultdict(list)
east_adjacency = defaultdict(list)

print("Calculating adjacencies")
for tile_id, tile_options in tiles.items():
    for i, tile in enumerate(tile_options):
        for inner_tile_id, inner_tile_options in tiles.items():
            if tile_id == inner_tile_id:
                continue

            for j, inner_tile in enumerate(inner_tile_options):
                if bottom(tile) == top(inner_tile):
                    south_adjacency[(tile_id, i)].append((inner_tile_id, j))
                if right(tile) == left(inner_tile):
                    east_adjacency[(tile_id, i)].append((inner_tile_id, j))
print("Calculated adjacencies")


def assemble(final_map, counter, size, available_tiles):
    # If there are no more available tiles, we're done!
    if len(available_tiles) == 0:
        print("found")
        return final_map

    # I don't remember which is which dimension and it shouldn't matter that
    # much - we're iterating in a specific order and width is equal to height.
    i = counter % size
    j = counter // size
    print("loc", size, i, j)

    # Look up our neighbors. Because we fill starting in the top-left, we only
    # need to check 2 neighbors.
    north_tile_id = final_map.get((i - 1, j))
    west_tile_id = final_map.get((i, j - 1))

    # If we're on the top or left edges, use all the possible tiles, otherwise
    # use our calculated adjacency maps.
    if north_tile_id is None:
        south_tiles = set()
        for tile_id in available_tiles:
            for offset, _ in enumerate(tiles[tile_id]):
                south_tiles.add((tile_id, offset))
    else:
        south_tiles = south_adjacency[north_tile_id]

    if west_tile_id is None:
        east_tiles = set()
        for tile_id in available_tiles:
            for offset, _ in enumerate(tiles[tile_id]):
                east_tiles.add((tile_id, offset))
    else:
        east_tiles = east_adjacency[west_tile_id]

    # XXX: We sort these so we always iterate in the same order. Mostly for
    # debugging at this point - it shouldn't be needed.
    target_tiles = [
        tile
        for tile in south_tiles
        if tile in east_tiles and tile[0] in available_tiles
    ]
    target_tiles.sort()

    print(len(final_map), len(available_tiles))

    # Loop through each possible target tile
    for tile_id, offset in target_tiles:
        print(tile_id, offset)
        tile = tiles[tile_id][offset]

        # Mark this tile as used, and set the value in the final_map before
        # recursing.
        available_tiles.remove(tile_id)
        final_map[(i, j)] = (tile_id, offset)

        tmp = assemble(
            final_map,
            counter + 1,
            size,
            available_tiles,
        )
        if tmp is not None:
            return final_map

        # If this wasn't the answer, mark this tile as not used, remove it from
        # the final map and carry on.
        available_tiles.add(tile_id)
        del final_map[(i, j)]

    return None


def part1(tiles):
    grid_size = isqrt(len(tiles))

    final_map = assemble({}, 0, grid_size, set(tiles.keys()))

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
