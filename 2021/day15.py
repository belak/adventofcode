import networkx as nx
from networkx.classes.function import path_weight

from adventlib import CARDINAL_DIRS as dirs, load_2d_grid

data = load_2d_grid("day15-input")


def populate_grid(data, G=None, multiplier=1):
    G = nx.DiGraph()
    G.add_node("start")
    G.add_edge("start", (0, 0), weight=0)
    G.add_edge(
        (len(data[0]) * multiplier - 1, len(data) * multiplier - 1),
        "end",
        weight=0,
    )

    for y in range(len(data) * multiplier):
        for x in range(len(data[0]) * multiplier):
            pos = (x, y)
            G.add_node(pos)

            for (dx, dy) in dirs:
                neighbor_pos = (x + dx, y + dy)
                if neighbor_pos[0] < 0 or neighbor_pos[0] >= len(data[0]) * multiplier:
                    continue
                if neighbor_pos[1] < 0 or neighbor_pos[1] >= len(data) * multiplier:
                    continue

                neighbor_grid_loc = (
                    neighbor_pos[0] // len(data[0]),
                    neighbor_pos[1] // len(data),
                )
                neighbor_sub_pos = (
                    neighbor_pos[0] % len(data[0]),
                    neighbor_pos[1] % len(data),
                )
                weight = (neighbor_grid_loc[0] + neighbor_grid_loc[1]) + data[
                    neighbor_sub_pos[1]
                ][neighbor_sub_pos[0]]
                if weight > 9:
                    weight -= 9

                G.add_edge(pos, neighbor_pos, weight=weight)

    return G


G = populate_grid(data)
path = nx.astar_path(G, "start", "end", weight="weight")
print(path_weight(G, path, "weight"))

G = populate_grid(data, G, multiplier=5)
path = nx.astar_path(G, "start", "end", weight="weight")
print(path_weight(G, path, "weight"))
