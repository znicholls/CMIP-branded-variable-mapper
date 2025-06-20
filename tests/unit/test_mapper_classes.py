"""
Tests of `cmip_branded_variable_mapper.mapper_classes`
"""

import re
from contextlib import nullcontext as does_not_raise

import pytest

from cmip_branded_variable_mapper.mapper_classes import (
    CellMethodsSubStringMapper,
    CellMethodsSubStringMapperOrdered,
)


@pytest.mark.parametrize(
    "sub_string_map, expectation",
    (
        pytest.param(
            {"time": "t1", "length": "l2", "weight": "w1"}, does_not_raise(), id="valid"
        ),
        pytest.param(
            {"time": "t1", "time1": "t2", "weight": "w1"},
            pytest.raises(
                AssertionError,
                match=re.escape(
                    "'time' is a subset of 'time1'. "
                    "You will need a different mapper or keys "
                    "to avoid incorrect results."
                ),
            ),
            id="clash",
        ),
    ),
)
def test_cell_methods_sub_string_mapper_validator(sub_string_map, expectation):
    with expectation:
        CellMethodsSubStringMapper(sub_string_map=sub_string_map)


@pytest.mark.parametrize(
    "sub_string_map, expectation",
    (
        pytest.param(
            (("time", "t1"), ("length", "l1"), ("weight", "w1")),
            does_not_raise(),
            id="valid",
        ),
        pytest.param(
            (("time", "t1"), ("time_longer", "t2"), ("weight", "w1")),
            pytest.raises(
                AssertionError,
                match=re.escape(
                    "'time' is a subset of 'time_longer'. "
                    "You will need to re-order your mapper to avoid incorrect results."
                ),
            ),
            id="invalid",
        ),
        pytest.param(
            (("time_longer", "t2"), ("time", "t1"), ("weight", "w1")),
            does_not_raise(),
            id="invalid_fixed",
        ),
    ),
)
def test_cell_methods_sub_string_mapper_ordered_validator(sub_string_map, expectation):
    with expectation:
        CellMethodsSubStringMapperOrdered(sub_string_map=sub_string_map)
