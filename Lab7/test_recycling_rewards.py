"""Property-based fuzz tests for recycling_rewards."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from recycling_rewards import parse_collection, weight_average, net_points


def _call_without_crashing(function, value):
    try:
        return function(value)
    except Exception as error:
        pytest.fail(f"{function.__name__} crashed with {type(error).__name__}: {error}")


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
def test_parse_collection_no_crash(value):
    result = _call_without_crashing(parse_collection, value)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], float)
    assert math.isfinite(result[1])
    assert result[1] >= 0


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
def test_weight_average_no_crash(value):
    result = _call_without_crashing(weight_average, value)
    assert isinstance(result, int)
    assert result >= 0


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
def test_net_points_no_crash(value):
    result = _call_without_crashing(net_points, value)
    assert isinstance(result, (int, float))
    assert math.isfinite(result)
    assert result >= 0


def test_parse_collection_keeps_valid_input_behavior():
    assert parse_collection(" paper:12 ") == ("Paper", 12.0)
    assert parse_collection("paper:not-a-number") == ("Unknown", 0.0)


def test_weight_average_keeps_valid_input_behavior():
    assert weight_average("5,12,20") == 12
    assert weight_average("") == 0


def test_net_points_keeps_valid_input_behavior():
    assert net_points("80|10") == 150.0
    assert net_points("2|100") == 0.0
