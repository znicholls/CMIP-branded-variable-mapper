"""
Test against the data request team's algorithm

The way the data request team have implemented this, you can't install it
(because it's in scripts not src).
You also can't import the script because the code runs on import
(hence will probably explode if it's not being run as a script).
As a result, I've just copied the relevant API here, good enough.
"""

import json
import re
import urllib.request

import pytest

from cmip_branded_variable_mapper import map_to_cmip_branded_variable


# # Old DR API, modified to make it easier to use without needing the variable class
# Source: https://github.com/CMIP-Data-Request/CMIP7_DReq_Software/blob/a466f0d4dddef9a3234134b1fc463f901135f37b/scripts/sandbox/create_brand_name.py#L40
# def compute_brand(variable, extended_brand_name=False):
#     var_name = str(variable.name)
#     param_name = str(variable.physical_parameter.name)
#     freq_name = str(variable.cmip7_frequency.name)
#     cell_methods = str(variable.cell_methods.cell_methods)
#     dimensions = str(variable.dimensions).split(", ")
def compute_brand_dr(  # noqa: PLR0912, PLR0913, PLR0915
    var_name: str,
    param_name: str,
    freq_name: str,
    cell_methods: str,
    dimensions: list[str],
    extended_brand_name: bool = False,
) -> str:
    # # Old API, modified to make it easier to use without needing the variable class
    # var_name = str(variable.name)
    # param_name = str(variable.physical_parameter.name)
    # freq_name = str(variable.cmip7_frequency.name)
    # cell_methods = str(variable.cell_methods.cell_methods)
    # dimensions = str(variable.dimensions).split(", ")
    # Temporal label
    if "time: max" in cell_methods or "time: min" in cell_methods:
        tlabel = "tstat"
    elif "time: sum" in cell_methods:
        tlabel = "tsum"
    elif "time" in dimensions or "timefxc" in dimensions:
        tlabel = "tavg"
    elif "time1" in dimensions:
        tlabel = "tpt"
    elif "time2" in dimensions:
        tlabel = "tclm"
    elif "time3" in dimensions:
        tlabel = "tclmdc"
    else:
        tlabel = "ti"
    # Vertical label
    vlabel = "u"
    if (
        "sdepth" in dimensions
        or "olevel" in dimensions
        or "alevel" in dimensions
        or "alevhalf" in dimensions
        or "olevhalf" in dimensions
    ):
        vlabel = "l"
    elif "rho" in dimensions:
        vlabel = "rho"
    else:
        height_pattern = r"^height(\d+)m$"
        depth_pattern = r"^((depth)|(olayer))(\d+)m?$"
        sdepth_pattern = r"^sdepth(\d+)$"
        opbar_pattern = r"^op(\d+)bar$"
        splevel_pattern = r"^pl?(\d+)$"
        alt_pattern = r"^alt(\d+)$"
        plevel_pattern = r"^plev(\d+[uch]?)$"
        oplevel_pattern = r"^oplev(\d+)$"
        height_dims = [
            dim
            for dim in dimensions
            if re.compile(height_pattern).match(dim) is not None
        ]
        depth_dims = [
            dim
            for dim in dimensions
            if re.compile(depth_pattern).match(dim) is not None
        ]
        sdepth_dims = [
            dim
            for dim in dimensions
            if re.compile(sdepth_pattern).match(dim) is not None
        ]
        opbar_dims = [
            dim
            for dim in dimensions
            if re.compile(opbar_pattern).match(dim) is not None
        ]
        splevel_dims = [
            dim
            for dim in dimensions
            if re.compile(splevel_pattern).match(dim) is not None
        ]
        alt_dims = [
            dim for dim in dimensions if re.compile(alt_pattern).match(dim) is not None
        ]
        plevel_dims = [
            dim
            for dim in dimensions
            if re.compile(plevel_pattern).match(dim) is not None
        ]
        oplevel_dims = [
            dim
            for dim in dimensions
            if re.compile(oplevel_pattern).match(dim) is not None
        ]
        if len(height_dims) > 0:
            vlabel = f"h{re.match(height_pattern, height_dims[0]).group(1)}m"
        elif len(sdepth_dims) > 0:
            vlabel = f"d{re.match(sdepth_pattern, sdepth_dims[0]).group(1)}0cm"
        elif len(depth_dims) > 0:
            vlabel = f"d{re.match(depth_pattern, depth_dims[0]).group(4)}m"
        elif len(opbar_dims) > 0:
            vlabel = f"op{re.match(opbar_pattern, opbar_dims[0]).group(1)}bar"
        elif len(splevel_dims) > 0:
            vlabel = f"{re.match(splevel_pattern, splevel_dims[0]).group(1)}hPa"
        elif len(alt_dims) > 0:
            vlabel = f"h{re.match(alt_pattern, alt_dims[0]).group(1)}"
        elif len(plevel_dims) > 0:
            vlabel = f"p{re.match(plevel_pattern, plevel_dims[0]).group(1)}"
        elif len(oplevel_dims) > 0:
            vlabel = f"op{re.match(oplevel_pattern, oplevel_dims[0]).group(1)}"
    # Horizontal label
    if (
        ("latitude" in dimensions and "longitude" in dimensions)
        or ("xant" in dimensions and "yant" in dimensions)
        or ("xgre" in dimensions and "ygre" in dimensions)
    ):
        hlabel = "hxy"
    elif (
        "latitude" in dimensions
        and "longitude" not in dimensions
        and "basin" not in dimensions
    ):
        hlabel = "hy"
    elif "site" in dimensions:
        hlabel = "hxys"
    elif "latitude" in dimensions and "basin" in dimensions:
        hlabel = "hys"
    elif (
        ("gridlatitude" in dimensions and "basin" in dimensions)
        or "oline" in dimensions
        or "siline" in dimensions
    ):
        hlabel = "ht"
    else:
        hlabel = "hm"
    # Area label
    if "where" not in cell_methods:
        alabel = "u"
    elif "air" in cell_methods:
        alabel = "air"
    elif "convective_cloud" in cell_methods:
        alabel = "ccl"
    elif "stratiform_cloud" in cell_methods:
        alabel = "scl"
    elif "cloud" in cell_methods:
        alabel = "cl"
    elif "crops" in cell_methods:
        alabel = "crp"
    elif "floating_ice_shelf" in cell_methods:
        alabel = "fis"
    elif "grounded_ice_sheet" in cell_methods:
        alabel = "gis"
    elif "ice_sheet" in cell_methods:
        alabel = "is"
    elif "ice_free_sea" in cell_methods:
        alabel = "ifs"
    elif "sea_ice_melt_pond" in cell_methods:
        alabel = "simp"
    elif "sea_ice_ridges" in cell_methods:
        alabel = "sir"
    elif "sea_ice" in cell_methods:
        alabel = "si"
    elif "sea" in cell_methods:
        alabel = "sea"
    elif "land_ice" in cell_methods:
        alabel = "li"
    elif "land" in cell_methods:
        alabel = "lnd"
    elif "natural_grasses" in cell_methods:
        alabel = "ng"
    elif "pastures" in cell_methods:
        alabel = "pst"
    elif "shrubs" in cell_methods:
        alabel = "shb"
    elif "snow" in cell_methods:
        alabel = "sn"
    elif "trees" in cell_methods:
        alabel = "tree"
    elif "unfrozen_soil" in cell_methods:
        alabel = "ufs"
    elif "vegetation" in cell_methods:
        alabel = "veg"
    elif "wetland" in cell_methods:
        alabel = "wl"
    elif "sector" in cell_methods:
        alabel = "multi"
    else:
        alabel = "undef"
    # Region
    if "xgre" in dimensions or "ygre" in dimensions or "Gre" in var_name:
        rlabel = "gre"
    elif "xant" in dimensions or "yant" in dimensions or "Ant" in var_name:
        rlabel = "ant"
    elif "site" in dimensions:
        rlabel = "site"
    else:
        rlabel = "global"
    rep = "-".join([param_name, tlabel, vlabel, hlabel, alabel])
    if extended_brand_name:
        return ".".join([rep, freq_name, rlabel])
    else:
        return rep


# A slightly stupid way to do this as you need an internet connection,
# but fine for now.
VARIABLE_URL = "https://raw.githubusercontent.com/CMIP-Data-Request/CMIP7_DReq_Software/a466f0d4dddef9a3234134b1fc463f901135f37b/scripts/examples/variables_v1.2.1.json"
with urllib.request.urlopen(VARIABLE_URL) as url:  # noqa: S310
    dr_variables = json.load(url)


dr_variable_info = pytest.mark.parametrize(
    "cn, info",
    [
        pytest.param(
            cn,
            info,
            id=cn,
        )
        for cn, info in dr_variables["Compound Name"].items()
    ],
)


@dr_variable_info
def test_compared_to_dr(cn, info):
    variable_name = info["physical_parameter_name"]
    cell_methods = info["cell_methods"]
    dimensions = info["dimensions"].split(" ")

    branded_variable_dr = compute_brand_dr(
        # Only used for region,
        # hence we don't care about the value for this comparison.
        var_name="junk",
        param_name=variable_name,
        freq_name=info["frequency"],
        cell_methods=cell_methods,
        dimensions=dimensions,
    )
    branded_variable_dr_components = branded_variable_dr.split("-")
    branded_variable_dr_corrected = "_".join(
        [
            branded_variable_dr_components[0],
            "-".join(branded_variable_dr_components[1:]),
        ]
    )

    branded_variable_here = map_to_cmip_branded_variable(
        variable_name=variable_name,
        cell_methods=cell_methods,
        dimensions=dimensions,
    )

    assert branded_variable_dr_corrected == branded_variable_here
