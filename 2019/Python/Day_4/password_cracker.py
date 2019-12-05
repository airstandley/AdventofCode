"""
Like a nutcracker that opens bank vaults.
"""

import os


def get_input(filepath):
    # Load the bounds
    with open(filepath) as f:
        upper_bound, lower_bound = (int(v) for v in f.readline().split("-"))
    return upper_bound, lower_bound


def check_password_is_valid(password):
    """
    Checks if a password is valid
    :param str -> password: a six digit (numbers only) string
    :return: bool
    """
    if len(password) != 6:
        return False

    doubles = set()
    voided_doubles = set()
    memory = [-1, -1]  # Now we have to track the last two digits
    for digit in password:
        try:
            digit = int(digit)
        except ValueError as e:
            return False  # Only numbers are allowed
        if digit == memory[0]:
            if digit == memory[1]:
                # If we there are three or more in a row it can't count for the double
                voided_doubles.add(digit)
            else:
                # It's a valid double
                doubles.add(digit)
        elif digit < memory[0]:
            return False  # Decreasing from the last digit is not allowed
        memory[1] = memory[0]
        memory[0] = digit
    if not (doubles - voided_doubles):
        return False  # At least one double digit is required.
    return True


def find_potential_passwords_in_range(lower_bound, upper_bound):
    passwords = []

    for password in range(lower_bound + 1, upper_bound):
        password = str(password)
        if check_password_is_valid(password):
            passwords.append(password)

    return passwords


def tests():
    assert check_password_is_valid("111111") is False
    assert check_password_is_valid("223450") is False
    assert check_password_is_valid("123789") is False

    assert check_password_is_valid("112233") is True
    assert check_password_is_valid("123444") is False
    assert check_password_is_valid("111122") is True
    assert check_password_is_valid("112233") is True
    print("Tests Passed")


if __name__ == "__main__":
    tests()
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    bounds = get_input(input_file)
    passwords = find_potential_passwords_in_range(*bounds)

    print(len(passwords))
