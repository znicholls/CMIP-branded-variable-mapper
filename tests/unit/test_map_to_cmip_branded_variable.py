"""
Tests of cmip_branded_variable_mapper.mapper
"""

from __future__ import annotations

import pytest

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


@pytest.mark.parametrize(
    "cell_methods, dimensions, exp_temporal_label",
    (
        pytest.param(
            "area: mean where land time: max",
            ("time", "lat", "lon"),
            # cell methods wins out over dimension
            "tmax",
            id="tmax",
        ),
        pytest.param(
            "area: mean where land time: min",
            ("time", "lat", "lon"),
            # cell methods wins out over dimension
            "tmin",
            id="tmin",
        ),
        pytest.param(
            "area: mean where land time: sum",
            ("time", "lat", "lon"),
            # cell methods wins out over dimension
            "tsum",
            id="tsum",
        ),
        pytest.param(
            "area: mean where land",
            ("time", "lat", "lon"),
            "tavg",
            id="tavg",
        ),
        pytest.param(
            "area: mean where land",
            ("time1", "lat", "lon"),
            "tpt",
            id="tpt",
        ),
        pytest.param(
            "area: mean where land",
            ("time2", "lat", "lon"),
            "tclm",
            id="tclm",
        ),
        pytest.param(
            "area: mean where land",
            ("time3", "lat", "lon"),
            "tclmdc",
            id="tclmdc",
        ),
        pytest.param(
            "area: mean where land",
            ("lat", "lon"),
            "ti",
            id="ti",
        ),
        pytest.param(
            "area: mean where land",
            ("time4", "lat", "lon"),
            "ti",
            id="ti-time4",
        ),
    ),
)
def test_temporal_labels(cell_methods, dimensions, exp_temporal_label):
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods=cell_methods,
        dimensions=dimensions,
    )

    exp = f"vname_{exp_temporal_label}-u-hm-lnd"

    assert res == exp


@pytest.mark.parametrize(
    "dimensions, exp_vertical_label",
    (
        (("latitude", "longitude", "olevel"), "ol"),
        (("latitude", "longitude", "olevhalf"), "olh"),
        (("latitude", "longitude", "alevel"), "al"),
        (("latitude", "longitude", "alevhalf"), "alh"),
        (("latitude", "longitude", "sdepth"), "sl"),
        (("latitude", "longitude", "sdepth10cm"), "d10cm"),
        (("latitude", "longitude", "sdepth100cm"), "d100cm"),
        (("latitude", "longitude", "depth0m"), "d0m"),
        (("latitude", "longitude", "depth100m"), "d100m"),
        (("latitude", "longitude", "depth300m"), "d300m"),
        (("latitude", "longitude", "depth700m"), "d700m"),
        (("latitude", "longitude", "depth1000m"), "d1000m"),
        (("latitude", "longitude", "depth2000m"), "d2000m"),
        (("latitude", "longitude", "olayer100m"), "d100m"),
        (("latitude", "longitude", "olayer300m"), "d300m"),
        (("latitude", "longitude", "olayer700m"), "d700m"),
        (("latitude", "longitude", "olayer2000m"), "d2000m"),
        (("latitude", "longitude", "op20bar"), "op20bar"),
        (("latitude", "longitude", "p925"), "925hPa"),
        (("latitude", "longitude", "plev5u"), "p5u"),
        (("latitude", "longitude", "plev6"), "p6"),
        (("latitude", "longitude", "oplayer4"), "op4"),
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
            (("gridlatitude", "basin"), "ht"),
            (("latitude", "basin"), "hys"),
            (("latitude",), "hy"),
            (("xant", "yant"), "hxy"),
            (("xgre", "ygre"), "hxy"),
            (("oline",), "ht"),
            (("siline",), "ht"),
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


@pytest.mark.parametrize(
    "cell_methods, exp_area_label",
    (
        ("area: mean (over land and sea ice) time: point", "lsi"),
        ("area: mean where cloud time: point", "cl"),
    ),
)
def test_area_labels(cell_methods, exp_area_label):
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods=cell_methods,
        dimensions=("latitude", "longitude", "time1"),
    )
    exp = f"vname_tpt-u-hxy-{exp_area_label}"

    assert res == exp


def test_where_sector():
    res = map_to_cmip_branded_variable(
        variable_name="vname",
        cell_methods="area: mean where sector",
        dimensions=("latitude", "longitude"),
    )

    exp = "vname_ti-u-hxy-multi"

    assert res == exp
