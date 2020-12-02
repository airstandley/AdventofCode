"""
I'm not particularly happy with the approach I hacked together.
Have read up a bit on computational geometry and visibility graphs,
going to try a cleaner approach
"""

EMPTY = "."
OBSTACLE = "#"


def get_obstacles(coordinate_grid):
    obstacles = set()
    for y, row in enumerate(coordinate_grid):
        for x, point in enumerate(row):
            if point == OBSTACLE:
                obstacles.add((x, y))


def is_visible(point_a, point_b, obstacles):
    return True


def build_visibility_graph(points, obstacles):
    # Build an undirected graph.
    graph = {}
    for view_point in points:
        edges = set()
        for target_point in points:
            # Check if target point is visible from view point
            # Need to research best way to do this. Some type of ray tracing?
            # Essentially we should construct a ray for each point and then find if that ray hits
            # an obstacle first.
            # Might be an optimization here?
            #   I.e. For a given ray we can learn the first obstacle it hits
            #       => Any other obstacles that share that ray are not visible from this point
            #           ==> This point is not visible from those obstacles
            #       => The first hit obstacle is visible from this point
            #           ==> This point is visible from that obstacle
            # Depending on the implementation, we might also learn all points the ray passes though before
            # and after the first obstacle which means we learn something about all those point's visibility
            # of the view point.
            # Not sure if that helps or not, but I intuitively feel like there must be should be some
            # advantage to using all the information you get from each ray solve.
            # For example to solve 1--->5
            #   If you have to calculate
            #       1--->X   5
            #   Then you also solve X-->1
            #
            #   If you have to calculate 1---2---3---4--->X    5
            #   Then you've also solved:
            #       2--->1, 2--->3, 2--->4, 2--->X, 3-->1, 3-->2, 3--->4, 3--->X, 4-->1, 4-->2, 4-->3, 4-->X,
            #       X--->4, X--->3, X--->2, and X--->1
            if is_visible(view_point, target_point, obstacles):
                edges.add(target_point)
        graph[view_point] = edges

    return graph


def find_best_station_location(asteroid_visibility_graph):
    max_visible_asteroids = 0
    best_locations = []
    for node, edges in asteroid_visibility_graph.items():
        visible_asteroids = len(edges)
        if visible_asteroids > max_visible_asteroids:
            max_visible_asteroids = visible_asteroids
            best_locations = [node]
        elif visible_asteroids == max_visible_asteroids:
            best_locations.append(node)
    return best_locations, max_visible_asteroids


def vaporize_asteroids(laser_location, asteroid_visibility_graph):
    killed_roids = []
    edges = asteroid_visibility_graph[laser_location]

    # Sort edges into counterclockwise order starting at (0,0)
    # edges = list(edges).sort(key=lambda x: do magic)
    for edge in edges:
        # Destroy the asteroid
        killed_roids.append(edge)
        # Ray trace to find any newly visible asteroids
        # new_edge = ray_trace(laser_location, direction_vector(laser_location, edge))
        # if new_edge:
        #     edges.append(new_edge)

    return killed_roids
