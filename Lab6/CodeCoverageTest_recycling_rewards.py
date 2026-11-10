"""Line-coverage test suite for recycling_rewards."""

import pytest

from recycling_rewards import collection_accepted, reward_points, slot_status


@pytest.mark.parametrize(
    "material,weight,bonus,expected",
    [
        ("paper", 3, False, 0),
        ("paper", 5, False, 0),
        ("paper", 5, True, 6),
        ("plastic", 3, False, 0),
        ("plastic", 4, True, 12),
        ("metal", 2, True, 0),
        ("metal", 3, True, 12),
        ("paper", 26, False, 210),
        ("metal", 23, False, 378),
    ],
)
def test_reward_points_valid_cases(material, weight, bonus, expected):
    assert reward_points(material, weight, bonus) == expected


@pytest.mark.parametrize(
    "material,weight,bonus,message",
    [("glass", 5, False, "unknown material"), ("paper", -1, False, "invalid weight")],
)
def test_reward_points_rejects_invalid_inputs(material, weight, bonus, message):
    with pytest.raises(ValueError, match=message):
        reward_points(material, weight, bonus)


@pytest.mark.parametrize(
    "weight,bags,hazardous,expected",
    [
        (5, 10, True, True),
        (6, 1, True, False),
        (50, 3, False, True),
        (51, 1, False, False),
        (20, 4, False, False),
    ],
)
def test_collection_acceptance_cases(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    "minutes,morning,holiday,expected",
    [
        (20, True, False, "open"),
        (19, True, False, "late"),
        (4, True, False, "missed"),
        (10, False, False, "open"),
        (9, False, False, "late"),
        (-6, False, False, "missed"),
        (35, True, True, "open"),
        (34, True, True, "late"),
        (19, False, True, "late"),
        (4, False, True, "missed"),
    ],
)
def test_slot_status_cases(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected
