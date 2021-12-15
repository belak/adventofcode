import networkx as nx
from networkx.classes.function import path_weight

data = open("day15-input").read().splitlines()
data = [list(map(int, line)) for line in data]

dirs = [
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0),
]

G = nx.DiGraph()

G.add_node("start")
G.add_node("end")

for y in range(len(data) * 5):
    for x in range(len(data[0]) * 5):
        pos = (x, y)
        G.add_node(pos)

        for (dx, dy) in dirs:
            neighbor_pos = (x + dx, y + dy)
            if neighbor_pos[0] < 0 or neighbor_pos[0] >= len(data[0]) * 5:
                continue
            if neighbor_pos[1] < 0 or neighbor_pos[1] >= len(data) * 5:
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

G1 = G.copy()
G1.add_edge("start", (0, 0), weight=0)
G1.add_edge((len(data[0]) - 1, len(data) - 1), "end", weight=0)
path = nx.shortest_path(G1, "start", "end", "weight")
print(path_weight(G1, path, "weight"))

G2 = G.copy()
G2.add_edge("start", (0, 0), weight=0)
G2.add_edge((len(data[0]) * 5 - 1, len(data) * 5 - 1), "end", weight=0)
path = nx.shortest_path(G2, "start", "end", "weight")
print(path_weight(G2, path, "weight"))
