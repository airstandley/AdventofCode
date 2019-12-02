import math
import os


def generate_input(filepath):
    # Create a generator that returns all module masses by reading from a newline delimited file
    with open(filepath) as f:
        for line in f:
            yield int(line)


def calculate_fuel_requirement(mass):
    # Calculate the fuel required for a given mass
    fuel = math.floor(mass / 3) - 2
    return fuel


def calculate_module_fuel_requirement(module_mass):
    required_fuel = total_fuel = 0
    remaining_mass = module_mass
    while remaining_mass > 0:
        remaining_mass = required_fuel = calculate_fuel_requirement(remaining_mass)
        if required_fuel > 0:
            total_fuel += required_fuel
    return total_fuel


def calculate_fuel_counter_upper(module_masses):
    return sum(map(calculate_module_fuel_requirement, module_masses))


if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    print(calculate_fuel_counter_upper(
        generate_input(input_file)
    ))
