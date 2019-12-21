from typing import List
import os
import itertools
import re
# Need to import Axes3D to register the 3d projection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import pyplot
import time


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


def efficent_simulation_tick(bodies):
    for i, a in enumerate(bodies):
        for b in bodies[i:]:
            if a.position.x < b.position.x:
                a.velocity.x += 1
                b.velocity.x -= 1
            elif a.position.x > b.position.x:
                a.velocity.x -= 1
                b.velocity.x += 1
            if a.position.y < b.position.y:
                a.velocity.y += 1
                b.velocity.y -= 1
            elif a.position.y > b.position.y:
                a.velocity.y -= 1
                b.velocity.y += 1
            if a.position.z < b.position.z:
                a.velocity.z += 1
                b.velocity.z -= 1
            elif a.position.z > b.position.z:
                a.velocity.z -= 1
                b.velocity.z += 1
    for body in bodies:
        body.position.x += body.velocity.x
        body.position.y += body.velocity.y
        body.position.z += body.velocity.z


def brute_force_it(bodies):
    history = set()
    history.add((hash(body) for body in bodies))
    tick = 0
    while True:
        simulation_tick(bodies)
        tick += 1
        print(tick)
        current = (hash(body) for body in bodies)
        if current in history:
            break
        history.add(current)
    return tick


def calculate_periods(bodies):
    # Had to cheat and look at redit.
    #  Had not though to consider that
    #   1) co-ordinates are all independent so you can find the cyclic period for each seperately
    #   2) If it's a cyclic pattern then the initial state will be the first to repeat so there's no reason to store
    #       past states
    x_initial = [(body.position.x, body.velocity.x) for body in bodies]
    y_initial = [(body.position.y, body.velocity.y) for body in bodies]
    z_initial = [(body.position.z, body.velocity.z) for body in bodies]

    x_period = None
    y_period = None
    z_period = None
    i = 0
    while x_period is None or y_period is None or z_period is None:
        efficent_simulation_tick(bodies)
        i += 1

        if not x_period and x_initial == [(body.position.x, body.velocity.x) for body in bodies]:
            print("X Match:", x_initial, [(body.position.x, body.velocity.x) for body in bodies])
            x_period = i
        if not y_period and y_initial == [(body.position.y, body.velocity.y) for body in bodies]:
            print("Y Match:", y_initial, [(body.position.y, body.velocity.y) for body in bodies])
            y_period = i
        if not z_period and z_initial == [(body.position.z, body.velocity.z) for body in bodies]:
            print("Z Match:", z_initial, [(body.position.z, body.velocity.z) for body in bodies])
            z_period = i
    return x_period, y_period, z_period


def find_least_common_multiple(values):
    i = 2  # Skip 1
    max_value = min(*values)
    while i <= max_value:
        for v in values:
            if v % i != 0:
                break
        else:
            return i
        i += 1
    return None


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
    efficent_simulation_tick(bodies)
    for body, expected in zip(bodies, expected_step_1):
        if body.position != expected.position:
            print("FAILED:", body.position, "!=", expected.position)
        if body.velocity != expected.velocity:
            print("FAILED:", body.velocity, "!=", expected.velocity)
        assert body.position == expected.position
        assert body.velocity == expected.velocity
    for _ in range(9):
        efficent_simulation_tick(bodies)
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

    # start_one = time.time()
    # for _ in range(10000):
    #     simulation_tick(bodies)
    # stop_one = time.time()
    #
    # start_two = time.time()
    # for _ in range(10000):
    #     efficent_simulation_tick(bodies)
    # stop_two = time.time()
    #
    # time_one = stop_one-start_one
    # time_two = stop_two-start_two
    #
    # print(time_one/10000*4000000000/60, time_two/10000*4000000000/60)

    # print(calculate_system_energy(bodies))

    # print(brute_force_it(bodies))

    values = calculate_periods(bodies)
    print(values)
    lcm = find_least_common_multiple(values)
    while lcm is not None:
        values = [v/lcm for v in values]
        lcm = find_least_common_multiple(values)
    print(values)
    x, y, z = values
    print(x*y*z)

