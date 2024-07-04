import random


def generate_random_number():
    return random.random()


def number_distance(n1, n2):
    return abs(n1 - n2)


def generate_distant_numbers(length, min_distance):
    numbers = []
    while len(numbers) < length:
        new_number = generate_random_number()
        if all(number_distance(new_number, existing_number) >= min_distance for existing_number in numbers):
            numbers.append(new_number)
    return numbers


def generate_fixed_distant_numbers(length):
    numbers = []

    colors_distance = random.choice([120, 45])
    first_color = random.random()
    numbers.append(first_color)
    color_angle = first_color * 360

    while len(numbers) < length:
        color_angle = (color_angle + colors_distance) % 360
        numbers.append(color_angle / 360)
    return numbers
