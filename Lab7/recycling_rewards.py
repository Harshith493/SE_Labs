"""Small, defensive helpers for recycling collection values and rewards."""

from math import isfinite


def parse_collection(text):
    """Parse a material:weight pair, returning a safe default if invalid."""
    if not isinstance(text, str) or text.count(":") != 1:
        return "Unknown", 0.0

    material_text, weight_text = text.split(":")
    material = material_text.strip().title()
    if not material:
        return "Unknown", 0.0

    try:
        weight = float(weight_text)
    except (ValueError, OverflowError):
        return "Unknown", 0.0

    if not isfinite(weight) or weight < 0:
        return "Unknown", 0.0
    return material, weight


def weight_average(weights_csv):
    """Return the whole-number average, or zero for invalid weight lists."""
    if not isinstance(weights_csv, str):
        return 0

    fields = weights_csv.split(",")
    if not fields or any(not field.strip() for field in fields):
        return 0

    try:
        values = [int(field.strip()) for field in fields]
    except (ValueError, OverflowError):
        return 0

    if any(value < 0 for value in values):
        return 0
    return sum(values) // len(values)


def net_points(text):
    """Return doubled points minus penalty, clamped to zero for invalid data."""
    if not isinstance(text, str) or text.count("|") != 1:
        return 0.0

    points_text, penalty_text = text.split("|")
    try:
        points = float(points_text)
        penalty = float(penalty_text)
    except (ValueError, OverflowError):
        return 0.0

    if not isfinite(points) or not isfinite(penalty):
        return 0.0
    if points < 0 or penalty < 0:
        return 0.0

    total = points * 2 - penalty
    if not isfinite(total):
        return 0.0
    return max(total, 0.0)


def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result)


if __name__ == "__main__":
    main()
