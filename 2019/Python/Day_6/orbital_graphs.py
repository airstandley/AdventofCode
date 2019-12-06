import os
import copy


def get_orbital_map(filepath):
    # Load the input
    orbits = []
    with open(filepath) as f:
        for line in f:
            orbits.append(line.rstrip().split(")"))
    return orbits


def generate_orbital_graph(orbital_map):
    # The problem seems like a directed graph so start by generating one.
    graph = {}
    for node, arc in orbital_map:
        graph.setdefault(node, [])
        graph[node].append(arc)
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


def tests():
    map_1 = [
        ['COM', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E'], ['E', 'F'], ['B', 'G'], ['G', 'H'],
        ['D', 'I'], ['E', 'J'], ['J', 'K'], ['K', 'L']
    ]
    assert calculate_orbits_counts(generate_orbital_graph(map_1)) == 42


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    orbital_map = get_orbital_map(input_file)
    orbital_graph = generate_orbital_graph(orbital_map)

    print(calculate_orbits_counts(orbital_graph))

