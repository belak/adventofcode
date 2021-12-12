import networkx as nx

data = [line.split("-") for line in open("day12-input").read().splitlines()]

G = nx.Graph()
G.add_edges_from(data)


# It's really a shame we have to do this, because networkx provides an
# all_simple_paths utility. Unfortunately, we need to be more careful about
# which nodes we exclude.
def find_all_paths(graph, start, end, part2=False):
    path = []
    paths = []
    raw_visited = {}
    visited = [start]

    # Start with one item in the queue - starting at the start node, ending at
    # the end, with nothing in the path and nothing visited.
    queue = [(start, end, path, visited, raw_visited)]

    while queue:
        start, end, path, visited, raw_visited = queue.pop()

        path = path + [start]

        # We need to track how many times we visited the smaller caves to solve
        # part2.
        if not start[0:1].isupper():
            if start not in raw_visited:
                raw_visited[start] = 0

            raw_visited[start] += 1

        # For part 1, all visited nodes actually count as visited.
        #
        # For part 2, all visited nodes count as visited only if there is at
        # least 1 node that has been visited 2 times.
        if part2:
            if 2 in raw_visited.values():
                visited = list(raw_visited.keys())
        else:
            visited = list(raw_visited.keys())

        # If we're at the end, we're done - no sense looping back on ourselves.
        # This fixes an issue in part2 where "end" could show up in the middle
        # of paths.
        if start == end:
            paths.append(path)
            continue

        # Attempt to search all adjacent nodes that don't count as "visited".
        for node in set(graph[start]).difference(visited):
            queue.append((node, end, path, visited.copy(), raw_visited.copy()))

    return paths


paths = find_all_paths(G, "start", "end")
print(len(list(paths)))

paths = find_all_paths(G, "start", "end", True)
print(len(list(paths)))
