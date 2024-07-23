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


def generate_stimulus_trial_two_rectangles(number_of_rectangles):
    assert number_of_rectangles == 2, "This function only works for two rectangles"

    selected_index = random.randint(0, number_of_rectangles - 1)
    colors = [0, 0]

    colors[selected_index] = random.random()
    distractor_distance = random.choice([0.33, 0.25, 0.16, -0.33, -0.25, -0.16])
    colors[1 - selected_index] = colors[selected_index] + distractor_distance
    if colors[1 - selected_index] > 1:
        colors[1 - selected_index] -= 1
    elif colors[1 - selected_index] < 0:
        colors[1 - selected_index] += 1

    return colors, selected_index, distractor_distance


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


def round_to_nearest(x):
    options = [60, 90, 120, -60, -90, -120]
    nearest = min(options, key=lambda option: abs(option - x))
    return nearest


def hue_to_degrees(hue):
    return hue * 360


def hue_difference_signed(reference, feedback):
    reference_degree = hue_to_degrees(reference)
    feedback_degree = hue_to_degrees(feedback)

    # Calculate signed difference
    difference_degrees = feedback_degree - reference_degree

    # Adjust difference to be within [-180, 180] degrees
    if difference_degrees > 180:
        difference_degrees -= 360
    elif difference_degrees < -180:
        difference_degrees += 360

    return difference_degrees
