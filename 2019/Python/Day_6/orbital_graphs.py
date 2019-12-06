import os
import copy


def get_orbital_map(filepath):
    # Load the input
    orbits = []
    with open(filepath) as f:
        for line in f:
            orbits.append(line.rstrip().split(")"))
    return orbits


def generate_directed_orbital_graph(orbital_map):
    # The problem seems like a directed graph so start by generating one.
    graph = {}
    for node, arc in orbital_map:
        graph.setdefault(node, [])
        graph[node].append(arc)
    return graph


def generate_undirected_orbital_graph(orbital_map):
    # When moving orbits we can go any direction so we want a undirected graph
    graph = {}
    for node, edge in orbital_map:
        graph.setdefault(node, [])
        graph.setdefault(edge, [])
        graph[node].append(edge)
        graph[edge].append(node)
    return graph


def calculate_orbits_counts(orbital_graph, node='COM', depth=0):
    # Recursively transverse though the graph counting the "orbits"
    orbits = depth  # All indirect orbits under this node
    if node in orbital_graph:
        orbiting_nodes = orbital_graph[node]
        for node in orbiting_nodes:
            orbits += calculate_orbits_counts(orbital_graph, node=node, depth=depth+1)
    else:
        # This is an edge node
        pass
    return orbits


def find_paths(orbital_graph, starting_node, ending_node, visited_nodes=None):
    """Recursively find all the paths from starting_node to ending_node in the graph
    Paths are returned as a list of paths, where paths are a list of nodes.
    An empty list means that no valid path exists.
    """
    path = copy.copy(visited_nodes) if visited_nodes else []
    if starting_node not in orbital_graph:
        return []  # We hit an dead end
    if starting_node in path:
        return []  # We hit a loop

    paths = []
    path.append(starting_node)
    for node in orbital_graph[starting_node]:
        if node == ending_node:
            # We've found it!
            path.append(node)
            paths.append(path)
        else:
            paths += find_paths(orbital_graph, node, ending_node, path)
    return paths


def calculate_shortest_path(orbital_graph, node_1='YOU', node_2='SAN'):

    valid_paths = find_paths(orbital_graph, node_1, node_2)

    lengths = [len(path) for path in valid_paths]
    shortest = min(lengths)
    # Subtract 2 since paths include the start and end nodes which are YOU and SAN and don't transfer
    # Subtract another 1 since the number of transfers is one less than the nodes
    return shortest - 3


def tests():
    map_1 = [
        ['COM', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E'], ['E', 'F'], ['B', 'G'], ['G', 'H'],
        ['D', 'I'], ['E', 'J'], ['J', 'K'], ['K', 'L']
    ]
    assert calculate_orbits_counts(generate_directed_orbital_graph(map_1)) == 42
    map_2 = [
        ['COM', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E'], ['E', 'F'], ['B', 'G'], ['G', 'H'], ['D', 'I'],
        ['E', 'J'], ['J', 'K'], ['K', 'L'], ['K', 'YOU'], ['I', 'SAN']
    ]
    assert calculate_shortest_path(generate_undirected_orbital_graph(map_2)) == 4


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    orbital_map = get_orbital_map(input_file)
    directed_orbital_graph = generate_directed_orbital_graph(orbital_map)
    print(calculate_orbits_counts(directed_orbital_graph))
    undirected_orbital_graph = generate_undirected_orbital_graph(orbital_map)
    print(calculate_shortest_path(undirected_orbital_graph))

