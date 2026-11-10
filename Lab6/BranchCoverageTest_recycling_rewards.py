"""Branch-coverage test suite for recycling_rewards."""

import pytest

from recycling_rewards import collection_accepted, reward_points, slot_status


@pytest.mark.parametrize(
    "material,weight,bonus,expected",
    [
        ("unknown", 1, False, None),  # Invalid material branch.
        ("paper", -1, False, None),  # Invalid weight branch.
        ("paper", 5, False, 0),  # No bonus, at the minimum.
        ("paper", 5, True, 6),  # Bonus lowers the minimum.
        ("metal", 2, True, 0),  # Metal bonus does not lower the minimum.
        ("plastic", 4, False, 6),  # Non-metal rate, ordinary extra weight.
        ("metal", 3, False, 12),  # Metal rate, ordinary extra weight.
        ("paper", 26, False, 210),  # High-weight non-metal rate adjustment.
        ("metal", 23, False, 378),  # High-weight metal rate adjustment.
    ],
)
def test_reward_points_branches(material, weight, bonus, expected):
    if material == "unknown":
        with pytest.raises(ValueError, match="unknown material"):
            reward_points(material, weight, bonus)
    elif weight < 0:
        with pytest.raises(ValueError, match="invalid weight"):
            reward_points(material, weight, bonus)
    else:
        assert reward_points(material, weight, bonus) == expected


@pytest.mark.parametrize(
    "weight,bags,hazardous,expected",
    [
        (5, 4, True, True),  # Hazardous and at the limit ignores bag count.
        (6, 1, True, False),  # Hazardous over the limit.
        (51, 1, False, False),  # Non-hazardous over the weight limit.
        (20, 4, False, False),  # Weight accepted, too many bags.
        (20, 3, False, True),  # Both non-hazardous checks pass.
    ],
)
def test_collection_accepted_branches(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    "minutes,morning,holiday,expected",
    [
        (20, True, False, "open"),  # Morning cutoff, open boundary.
        (19, True, False, "late"),  # Morning late interval.
        (4, True, False, "missed"),  # Below morning late interval.
        (10, False, False, "open"),  # Afternoon cutoff, open boundary.
        (9, False, False, "late"),  # Afternoon late interval.
        (-6, False, False, "missed"),  # Below afternoon late interval.
        (35, True, True, "open"),  # Holiday raises morning cutoff.
        (34, True, True, "late"),  # Holiday morning late interval.
        (25, False, True, "open"),  # Holiday raises afternoon cutoff.
        (18, False, True, "late"),  # Holiday afternoon late interval.
        (3, False, True, "missed"),  # Holiday missed branch.
    ],
)
def test_slot_status_branches(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected
