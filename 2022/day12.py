from adventlib import AOC

import numpy as np
import networkx as nx


def can_travel_from(src, dest):
    diff = ord(dest) - ord(src)
    return diff <= 1


class Day12(AOC):
    def process_input(self, raw_data):
        data = np.array([list(line) for line in raw_data.splitlines()])

        self.start_point = tuple(np.argwhere(data == "S")[0])
        self.end_point = tuple(np.argwhere(data == "E")[0])

        # Replace the start and end points with the values they represent.
        data[self.start_point] = "a"
        data[self.end_point] = "z"

        self.graph = nx.DiGraph()

        # We create a digraph from a grid and iterate over the edges - it's less
        # error prone (and less code) than looping through the ranges ourselves.
        for (src, dest) in nx.grid_2d_graph(*data.shape).to_directed().edges():
            if can_travel_from(data[src], data[dest]):
                self.graph.add_edge(src, dest)

        return data

    def part1(self):
        return nx.shortest_path_length(self.graph, self.start_point, self.end_point)

    def part2(self):
        # Find all points with a value of "a".
        starting_points = set(map(tuple, np.argwhere(self.data == "a")))

        # We can use shortest_path_length to find all possible routes to the
        # target, so we start there and filter it to the starting points we
        # previously found.
        possible_paths = [
            v
            for k, v in nx.shortest_path_length(
                self.graph, target=self.end_point
            ).items()
            if k in starting_points
        ]

        return min(possible_paths)


if __name__ == "__main__":
    aoc = Day12()
    aoc.run()
