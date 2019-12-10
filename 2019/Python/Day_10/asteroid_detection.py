import os
import copy
import math


EMPTY = "."
ASTEROID = "#"
OBSCURED = "?"


def generate_map_from_data(asteroid_map_data):
    asteroid_map = []
    for row in asteroid_map_data:
        map_row = []
        for co_ordinate in row:
            map_row.append(co_ordinate)
        asteroid_map.append(map_row)
    return asteroid_map


def get_asteroid_map(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    with open(filepath) as f:
        data = [line.strip() for line in f]
    return generate_map_from_data(data)


def find_line_of_sight_points(asteroid_map, coordinates, line_of_sight_vector):
    points = []
    y_min = -1
    y_max = len(asteroid_map)
    x_min = -1
    x_max = len(asteroid_map[0])
    x, y = coordinates
    while True:
        x, y = x + line_of_sight_vector[0], y + line_of_sight_vector[1]
        if (y_min < y < y_max) and (x_min < x < x_max):
            points.append((x,y))
        else:
            # Search is done
            return points


def block_off_line_of_sight(asteroid_map, coordinates, line_of_sight_vector):
    points = find_line_of_sight_points(asteroid_map, coordinates, line_of_sight_vector)
    for point in points:
        x, y = point
        asteroid_map[y][x] = OBSCURED


def reduce_vector(vector):
    """
    Given a vector remove all common divisors so that it's a "integer unit vector"
    """
    x, y = vector
    if x == 0:
        y = y/abs(y)
    elif y == 0 :
        x = x/abs(x)
    else:
        while True:
            for i in range(1, min(abs(x), abs(y)) + 1):
                if x % i == 0 and y % i == 0 and i != 1:
                    x, y = x/i, y/i
                    break
            else:
                break
    return (x, y)


def calculate_visible_points(asteroid_map, coordinates):
    """
    Counts visible asteroids while finding out what spaces are blocked by line-of-sight
    Example of asteroids blocking observability:
    #.........
    ...A......
    ...B..a...
    .EDCG....a
    ..F.c.b...
    .....c....
    ..efd.c.gb
    .......c..
    ....f...c.
    ...e..d..c
    """
    blocked_map = copy.deepcopy(asteroid_map)
    blocked_map[coordinates[1]][coordinates[0]] = "X"
    y_min = -1
    y_max = len(asteroid_map)
    x_min = -1
    x_max = len(asteroid_map[0])
    max_distance = max(x_max, y_max)
    distance = 1
    while distance <= max_distance:
        for y_offset in range(-distance, distance+1):
            for x_offset in range(-distance, distance + 1):
                if y_offset == 0 and x_offset == 0:
                    continue
                x = coordinates[0] + x_offset
                y = coordinates[1] + y_offset
                if (y_min < y < y_max) and (x_min < x < x_max):
                    direction_vector = [x_offset, y_offset]
                    if blocked_map[y][x] == ASTEROID:
                        block_off_line_of_sight(blocked_map, (x,y), reduce_vector(direction_vector))
        distance += 1
    return blocked_map


def view_count(asteroid_map, coordinates):
    blocked_map = calculate_visible_points(asteroid_map, coordinates)
    visible_count = 0
    for row in blocked_map:
        for point in row:
            if point == ASTEROID:
                visible_count += 1
    return visible_count


def determine_best_monitor_location(asteroid_map):
    max_view_count = 0
    best_location = None

    for y, row in enumerate(asteroid_map):
        for x, space in enumerate(row):
            if space == ASTEROID:
                asteroids_in_view = view_count(asteroid_map, (x,y))
                if asteroids_in_view > max_view_count:
                    max_view_count = asteroids_in_view
                    best_location = (x,y)
    return best_location, max_view_count


def fire_laser(asteroid_map, location, vector):
    points = find_line_of_sight_points(asteroid_map, location, vector)

    if points:
        for y, row in enumerate(asteroid_map):
            output = []
            for x, space in enumerate(row):
                output.append("*" if (x,y) in points else space)
            print(output)
    for point in points:
        if point == ASTEROID:
            print("BOOM ", point)
            return point
    return None


def vaporize_asteroids(asteroid_map, station_location):
    updated_map = copy.deepcopy(asteroid_map)
    updated_map[station_location[1]][station_location[0]] = "X"
    hits = []

    def determine_hit(x, y):
        if x == 0 and y == 0:
            return
        direction_vector = reduce_vector((x, y))
        print("Checking", direction_vector, x, y)
        hit_roid = fire_laser(updated_map, station_location, direction_vector)
        if hit_roid:
            hits.append(hit_roid)
            updated_map[hit_roid[1]][hit_roid[0]] = EMPTY

    # Rotate around clockwise starting at (0,1)
    # Increment by the smallest possible vector (0,0) to (max_y, max_x)??
    # I DONT KNOW HOW TO DO THIS AAAARTGAGASER
    max_y = len(asteroid_map)
    max_x = len(asteroid_map[0])
    max_vector = max(max_x, max_y)
    while True:
        # FIRING MY LAZER!!!!!!
        y_offset = -max_vector
        x_offset = 0
        hit_count = len(hits)
        # I don't know how to rotate clockwise well....
        while x_offset <= max_vector:
            determine_hit(x_offset, y_offset)
            x_offset += 1
        while y_offset <= max_vector:
            y_offset += 1
            determine_hit(x_offset, y_offset)
        while x_offset >= -max_vector:
            x_offset += -1
            determine_hit(x_offset, y_offset)
        while y_offset >= -max_vector:
            y_offset += -1
            determine_hit(x_offset, y_offset)
        if len(hits) == hit_count:
            # Were done
            return hits


def tests():
    asteroid_map_data = generate_map_from_data([
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##"
    ])
    assert view_count(asteroid_map_data, (3,4)) == 8
    assert view_count(asteroid_map_data, (1,0)) == 7
    assert view_count(asteroid_map_data, (4,0)) == 7
    assert determine_best_monitor_location(asteroid_map_data)[0] == (3,4)

    print("Tests Done")


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    asteroid_map = get_asteroid_map(input_file)

    # location, view_count = determine_best_monitor_location(asteroid_map)
    # print(location, view_count)
    location = (19, 11)
    hits = vaporize_asteroids(asteroid_map, location)
    asteroid_200 = hits[199]
    print(asteroid_200[0]*10 + asteroid_200[1])
