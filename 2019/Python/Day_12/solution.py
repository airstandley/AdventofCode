from typing import List
import os
import itertools
import re
# Need to import Axes3D to register the 3d projection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import pyplot


from utils.grid_tools_3d import Point3D, Vector3D, Body3D


def get_input(filepath):
    input_regex = re.compile(r'<x=([-\d]*), y=([-\d]*), z=([-\d]*)>')
    with open(filepath) as f:
        data = [input_regex.match(line.strip()).groups() for line in f]
    return data


def get_bodies(data):
    bodies = []
    for i, groups in enumerate(data):
        bodies.append(Body3D(position=Point3D(*[int(i) for i in groups]), label=chr(i+65)))
    return bodies

tick = 0


def simulation_tick(bodies, debug=False, plot=False):
    # Zero Acceleration
    for body in bodies:
        body.acceleration = Vector3D()
    # Apply gravity
    update_acceleration_from_gravity(bodies)
    update_velocity(bodies)
    # Apply velocity
    update_position(bodies)

    if debug:
        # Print position
        global tick
        tick += 1
        print("Tick", tick)
        for body in bodies:
            print(body)
        print()

    if plot:
        # Plot position
        plot_bodies(bodies)


def calculate_gravity(a: Body3D, b: Body3D):
    """
    Calculate the acceleration of body A due to the force of gravity applied by body B.
    """
    def gravity(pos_a, pos_b):
        if pos_a < pos_b:
            return 1
        elif pos_a > pos_b:
            return -1
        else:
            return 0
    return Vector3D(
        x=gravity(a.position.x, b.position.x),
        y=gravity(a.position.y, b.position.y),
        z=gravity(a.position.z, b.position.z)
    )


def update_acceleration_from_gravity(bodies: List[Body3D]):
    """
    Updates the acceleration on the given bodies based on the effects of gravity.
    :param bodies: List of Body3D objects.
    """
    pairs = itertools.combinations(bodies, 2)
    for a, b in pairs:
        a.acceleration += calculate_gravity(a, b)
        b.acceleration += calculate_gravity(b, a)


def update_velocity(bodies: List[Body3D]):
    for body in bodies:
        body.velocity += body.acceleration


def update_position(bodies: List[Body3D]):
    for body in bodies:
        body.position += body.velocity


fig = pyplot.figure()
ax = fig.add_subplot(projection='3d')


def plot_bodies(bodies):
    xs = []
    ys = []
    zs = []
    for body in bodies:
        position = [body.position.x, body.position.y, body.position.z]
        velocity = [body.velocity.direction.x, body.velocity.direction.y, body.velocity.direction.z]
        acceleration = [body.acceleration.direction.x, body.acceleration.direction.y, body.acceleration.direction.z]
        ax.scatter(*position)
        ax.quiver(*position, *velocity, color='green')
        ax.quiver(*position, *acceleration, color='red')
        if body.label is not None:
            ax.text(*position, body.label)


def calculate_potential_energy(body):
    return abs(body.position.x) + abs(body.position.y) + abs(body.position.z)


def calculate_kinetic_energy(body):
    return abs(body.velocity.x) + abs(body.velocity.y) + abs(body.velocity.z)


def calculate_total_energy(body):
    return calculate_potential_energy(body) * calculate_kinetic_energy(body)


def calculate_system_energy(bodies):
    total_energy = 0
    for body in bodies:
        total_energy += calculate_total_energy(body)
    return total_energy


def tests():
    bodies = [
        Body3D(position=Point3D(x=-1, y=0, z=2), label="A"),
        Body3D(position=Point3D(x=2, y=-10, z=-7), label="B"),
        Body3D(position=Point3D(x=4, y=-8, z=8), label="C"),
        Body3D(position=Point3D(x=3, y=5, z=-1), label="D")
    ]
    expected_step_1 = [
        Body3D(position=Point3D(x=2, y=-1, z=1), velocity=Vector3D(x=3, y=-1, z=-1)),
        Body3D(position=Point3D(x=3, y=-7, z=-4), velocity=Vector3D(x=1, y=3, z=3)),
        Body3D(position=Point3D(x=1, y=-7, z=5), velocity=Vector3D(x=-3, y=1, z=-3)),
        Body3D(position=Point3D(x=2, y=2, z=0), velocity=Vector3D(x=-1, y=-3, z=1))
    ]
    expected_step_10 = [
        Body3D(position=Point3D(x=2, y=1, z=-3), velocity=Vector3D(x=-3, y=-2, z=1)),
        Body3D(position=Point3D(x=1, y=-8, z=0), velocity=Vector3D(x=-1, y=1, z=3)),
        Body3D(position=Point3D(x=3, y=-6, z=1), velocity=Vector3D(x=3, y=2, z=-3)),
        Body3D(position=Point3D(x=2, y=0, z=4), velocity=Vector3D(x=1, y=-1, z=-1))
    ]
    simulation_tick(bodies)
    for body, expected in zip(bodies, expected_step_1):
        if body.position != expected.position:
            print("FAILED:", body.position, "!=", expected.position)
        if body.velocity != expected.velocity:
            print("FAILED:", body.velocity, "!=", expected.velocity)
        assert body.position == expected.position
        assert body.velocity == expected.velocity
    for _ in range(9):
        simulation_tick(bodies)
    for body, expected in zip(bodies, expected_step_10):
        if body.position != expected.position:
            print("FAILED:", body.position, "!=", expected.position)
        if body.velocity != expected.velocity:
            print("FAILED:", body.velocity, "!=", expected.velocity)
        assert body.position == expected.position
        assert body.velocity == expected.velocity

    assert calculate_system_energy(bodies) == 179

    # Just check a second set has the expected final system energy
    bodies = [
        Body3D(position=Point3D(x=-8, y=-10, z=0)),
        Body3D(position=Point3D(x=5, y=5, z=10)),
        Body3D(position=Point3D(x=2, y=-7, z=3)),
        Body3D(position=Point3D(x=9, y=-8, z=-3))
    ]
    for _ in range(100):
        simulation_tick(bodies)

    assert calculate_system_energy(bodies) == 1940

    print("Tests Done")


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    bodies = get_bodies(get_input(input_file))

    for _ in range(1000):
        simulation_tick(bodies)

    print(calculate_system_energy(bodies))

