"""
Tests of  cmip_branded_variable_mapper.mapper
"""

from __future__ import annotations

import pytest

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


@pytest.mark.parametrize(
    "dimensions, exp_vertical_label",
    (
        (("latitude", "longitude", "sdepth1"), "d10cm"),
        (("latitude", "longitude", "sdepth10"), "d1m"),
        (("latitude", "longitude", "depth0m"), "d0m"),
        (("latitude", "longitude", "depth100m"), "d100m"),
        (("latitude", "longitude", "olayer100m"), "d100m"),
        (("latitude", "longitude", "olayer300m"), "d300m"),
        (("latitude", "longitude", "olayer700m"), "d700m"),
        (("latitude", "longitude", "olayer2000m"), "d2000m"),
        (("latitude", "longitude", "op20bar"), "op20bar"),
        (("latitude", "longitude", "p925"), "925hPa"),
        (("latitude", "longitude", "plev5u"), "p5u"),
        (("latitude", "longitude", "plev6"), "p6"),
        (("latitude", "longitude", "oplev4"), "op4"),
    ),
)
def test_vertical_labels(dimensions, exp_vertical_label):
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods="area: mean where air",
        dimensions=dimensions,
    )

    exp = f"vname_ti-{exp_vertical_label}-hxy-air"

    assert res == exp


@pytest.mark.parametrize(
    "dimensions, exp_horizontal_label",
    (
        pytest.param(
            dimensions,
            exp_horizontal_label,
            id=f"{'-'.join(dimensions)}_{exp_horizontal_label}",
        )
        for dimensions, exp_horizontal_label in (
            (("longitude", "latitude"), "hxy"),
            (("gridlatitude", "basin"), "Ht"),
            (("latitude", "basin"), "hys"),
            (("latitude",), "hy"),
            (("xant", "yant"), "hxy"),
            (("xgre", "ygre"), "hxy"),
            (("oline",), "Ht"),
            (("siline",), "Ht"),
            (("site",), "hxys"),
        )
    ),
)
def test_horizontal_labels(dimensions, exp_horizontal_label):
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods="area: mean where air",
        dimensions=dimensions,
    )

    exp = f"vname_ti-u-{exp_horizontal_label}-air"

    assert res == exp


def test_where_sector():
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods="area: mean where sector",
        dimensions=("latitude", "longitude"),
    )

    exp = "vname_ti-u-hxy-multi"

    assert res == exp
