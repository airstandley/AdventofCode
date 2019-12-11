import os
import copy
import math


EMPTY = "."
ASTEROID = "#"
OBSCURED = "?"


# Extend Point and Vector from Day 3
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point({},{})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Cannot add Point and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise ValueError("Cannot subtract Point and {}".format(type(other)))


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def direction(self):
        # Return the unit/directoinal vector for this vector
        return Vector(self.x/self.magnitude, self.y/self.magnitude)

    def dot_product(self, other):
        # X1*X2+Y1*Y2+Z1*Z2......
        return self.x * other.x + self.y * other.y

    def angle(self, other=None):
        # Angle between this vector and (optionally) other
        angle = math.degrees(math.atan2(self.y, self.x)) + 180
        # atan2 returns -pi/2(-180) to pi/2(180) we want it to return 0 - pi(360)
        if other:
            angle = angle - other.angle()
        return angle

    # def alt_angle(self, other):
    #     angle = math.acos(
    #         self.dot_product(other)/(self.magnitude * other.magnitude)
    #     )
    #     return math.degrees(angle)

    # def nearest_integer(self):
    #     # Return the nearest vector with only integer components
    #     return Vector(int(self.x), int(self.y))

    def reduce(self):
        """
        Given a vector remove all common divisors so that it's a "integer unit vector"
        """
        if self.x == 0 and self.y == 0:
            x, y = self.x, self.y
        elif self.x == 0:
            x = self.x
            y = self.y / abs(self.y)
        elif self.y == 0:
            x = self.x / abs(self.x)
            y = self.y
        else:
            x, y = self.x, self.y
            while True:
                for i in range(1, min(abs(x), abs(y)) + 1):
                    if x % i == 0 and y % i == 0 and i != 1:
                        x, y = x / i, y / i
                        break
                else:
                    break
        return Vector(x, y)

    def __repr__(self):
        return "Vector({},{})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dot_product(other)
        else:
            return super().__mul__(other)


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


def calculate_all_line_of_sight_vectors(asteroid_map, coordinates):
    """Generate a set of all the vectors that are possible in the given grid from coordinates
    A 'possible' vector is one that passes through at least one other point
    """
    vectors = set()
    # Cheat by starting at the 'other point'
    y_max = len(asteroid_map)
    x_max = len(asteroid_map[0])
    max_distance = max(x_max, y_max)
    distance = 1
    while distance <= max_distance:
        for y_offset in range(-distance, distance + 1):
            for x_offset in range(-distance, distance + 1):
                if y_offset == 0 and x_offset == 0:
                    continue
                x = coordinates[0] + x_offset
                y = coordinates[1] + y_offset
                if (0 <= y < y_max) and (0 <= x < x_max):
                    direction_vector = Vector(x_offset, y_offset)
                    vectors.add(direction_vector.reduce())
        distance += 1
    return vectors


def find_line_of_sight_points(asteroid_map, coordinates, line_of_sight_vector):
    points = []
    y_min = -1
    y_max = len(asteroid_map)
    x_min = -1
    x_max = len(asteroid_map[0])
    x, y = coordinates
    while True:
        x, y = x + line_of_sight_vector.x, y + line_of_sight_vector.y
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
                    los_vector = Vector(x_offset, y_offset)
                    if blocked_map[y][x] == ASTEROID:
                        block_off_line_of_sight(blocked_map, (x,y), los_vector.reduce())
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
    print("Firing at", vector)
    points = find_line_of_sight_points(asteroid_map, location, vector)

    if points:
        for y, row in enumerate(asteroid_map):
            output = []
            for x, space in enumerate(row):
                if (x,y) in points:
                    if space == ASTEROID:
                        output.append("!")
                    else:
                        output.append("*")
                else:
                    output.append(space)
            print(output)
    for point in points:
        x, y = point
        if asteroid_map[y][x] == ASTEROID:
            print("BOOM ", point)
            return point
    return None


def sort_sight_vectors_into_clockwise(vectors):
    base_vector = Vector(0, -1)
    vectors.sort(key=lambda v: v.angle(base_vector))
    return vectors


def vaporize_asteroids(asteroid_map, station_location):
    updated_map = copy.deepcopy(asteroid_map)
    updated_map[station_location[1]][station_location[0]] = "X"
    hits = []

    sight_vectors = list(calculate_all_line_of_sight_vectors(asteroid_map, station_location))
    sort_sight_vectors_into_clockwise(sight_vectors)
    while True:
        # FIRING MY LAZER!!!!!!
        hit_count = len(hits)  # Track the starting hit count
        # Rotate around clockwise starting at (0,-1)
        for los_vector in sight_vectors:
            hit_roid = fire_laser(updated_map, station_location, los_vector)
            if hit_roid:
                hits.append(hit_roid)
                updated_map[hit_roid[1]][hit_roid[0]] = EMPTY

        if len(hits) == hit_count:
            # We didn't hit anything so we are done
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
    print(asteroid_200[0]*100 + asteroid_200[1])
