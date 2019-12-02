import math
import os


def generate_input(filepath):
    # Create a generator that returns all module masses by reading from a newline delimited file
    with open(filepath) as f:
        for line in f:
            yield int(line)


def calculate_module_fuel_requirement(module_mass):
    # Calculate the fuel required for a module given it's mass
    module_fuel = math.floor(module_mass / 3) - 2
    return module_fuel


def calculate_fuel_counter_upper(module_masses):
    return sum(map(calculate_module_fuel_requirement, module_masses))


if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    print(calculate_fuel_counter_upper(
        generate_input(input_file)
    ))
