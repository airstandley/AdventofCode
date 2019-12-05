import os
from matplotlib import pyplot

MAX_DISTANCE = 999999999999999


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
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def generate_wire_coordinates(instructions):
    # Calculate all the points on the grid for a wire based on a set of directional instructions.
    coordinates = []

    # Start at the origin
    current_point = Point(x=0, y=0)

    direction_switch = {
        "R": Vector(x=1),
        "L": Vector(x=-1),
        "D": Vector(y=-1),
        "U": Vector(y=1)
    }

    for direction, amount in instructions:
        for _ in range(int(amount)):
            current_point += direction_switch[direction]
            coordinates.append(current_point)

    return coordinates


def get_wires(filepath):
    # Load the comma separated intcode program from a file into memory (a list).
    wires = []
    with open(filepath) as f:
        for line in f:
            instructions = [(a[0], a[1:]) for a in line.split(",")]
            wires.append(generate_wire_coordinates(instructions))
    return wires


def calculate_closest_cross_point(wire_1, wire_2):
    # Find all intersection points using sets
    wire_1_unique = set(wire_1)
    wire_2_unique = set(wire_2)
    intersection = wire_1_unique.intersection(wire_2_unique)

    # Find the closest one
    closest_distance = MAX_DISTANCE
    closest_point = Point(0, 0)
    for point in intersection:
        distance = abs(point.x) + abs(point.y)
        if distance < closest_distance:
            closest_distance = distance
            closest_point = point
    return closest_distance, closest_point


def tests():
    a1 = generate_wire_coordinates([(i[0], i[1:]) for i in "R8,U5,L5,D3".split(",")])
    a2 = generate_wire_coordinates([(i[0], i[1:]) for i in "U7,R6,D4,L4".split(",")])
    assert calculate_closest_cross_point(a1, a2)[0] == 6
    b1 = generate_wire_coordinates([(i[0], i[1:]) for i in "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")])
    b2 = generate_wire_coordinates([(i[0], i[1:]) for i in "U62,R66,U55,R34,D71,R55,D58,R83".split(",")])
    assert calculate_closest_cross_point(b1, b2)[0] == 159
    c1 = generate_wire_coordinates([(i[0], i[1:]) for i in "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R5".split(",")])
    c2 = generate_wire_coordinates([(i[0], i[1:]) for i in "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")])
    assert calculate_closest_cross_point(c1, c2)[0] == 135
    print("Tests Passed")


if __name__ == "__main__":
    tests()
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")

    wire1, wire2 = get_wires(input_file)

    print([p for p in wire1 if p.y == -154])
    print([p for p in wire1 if p.x == -154])
    print([p for p in wire1 if hash(p) == hash(Point(-154, 0))])

    x_1, y_1 = zip(*[(p.x, p.y) for p in wire1])
    x_2, y_2 = zip(*[(p.x, p.y) for p in wire2])

    pyplot.plot(x_1, y_1, 'ro')
    pyplot.plot(x_2, y_2, 'bo')
    pyplot.axis([-200, 200, -200, 200])
    pyplot.show()

    print(Point(-154, 0) in wire1, Point(-154, 0) in wire2)
    distance, point = calculate_closest_cross_point(wire1, wire2)
    print(distance, point)
