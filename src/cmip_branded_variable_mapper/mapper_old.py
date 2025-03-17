"""
Mapper from old names to branded variables

This is based on the definitions in the spreadsheet for now,
the long-term source of truth is still being figured out
(https://github.com/znicholls/CMIP-branded-variable-mapper/issues/4).
"""

from __future__ import annotations

time_labels_dimensions = {
    "time": "tavg",
    "time1": "tpt",
    "time2": "tcla",
    "time3": "tcld",
}


time_labels_cell_methods = {
    "time: max": "tstat",
    "time: min": "tstat",
    "time: sum": "tsum",
}


vertical_labels = {
    "sdepth": "l",
    "olevel": "l",
    "alevel": "l",
    "alevhalf": "l",
    "olevhalf": "l",
    "rho": "rhon",
    "height2m": "h02",
    "height10m": "h010",
    "height100m": "h0100",
    "sdepth1": "z0p1",
    "sdepth10": "z01",
    "depth0m": "z00",
    "depth100m": "z0100",
    "olayer100m": "z0100",
    "olayer300m": "z0300",
    "olayer700m": "z0700",
    "olayer2000m": "z02000",
    "p10": "p010",
    "p100": "p0100",
    "p220": "p0220",
    "p500": "p0500",
    "p560": "p0560",
    "p700": "p0700",
    "pl700": "p0700",
    "p840": "p0840",
    "p850": "p0850",
    "p1000": "p01000",
    "alt16": "h16",
    "alt40": "h40",
    "plev3": "p3",
    "plev4": "p4",
    "plev8": "p8",
    "plev7c": "p7c",
    "plev7h": "p7h",
    "plev19": "p19",
    "plev27": "p27",
    "plev39": "p39",
}



horizontal_labels = {
    ("longitude", "latitude"): "hxy",
    ("gridlatitude", "basin"): "ht",
    ("latitude", "basin"): "hys",
    ("latitude",): "hy",
    ("xant", "yant"): "hxy",
    ("xgre", "ygre"): "hxy",
    ("oline",): "ht",
    ("siline",): "ht",
    ("site",): "hxys",
}


area_labels = {
    "where air": "air",
    "where cloud": "cl",
    "where convective_cloud": "ccl",
    "where crops": "crp",
    "where floating_ice_shelf": "fis",
    "where grounded_ice_sheet": "gis",
    "where ice_free_sea": "ifs",
    "where ice_sheet": "is",
    "where land": "lnd",
    "where land_ice": "li",
    "where natural_grasses": "ng",
    "where pastures": "pst",
    "where sea": "sea",
    "where sea_ice": "si",
    "where sea_ice_melt_pond": "simp",
    "where sea_ice_ridges": "sir",
    "where sector": "lus",
    "where shrubs": "shb",
    "where snow": "sn",
    "where stratiform_cloud": "scl",
    "where trees": "tree",
    "where unfrozen_soil": "ufs",
    "where vegetation": "veg",
    "where wetland": "wl",
}


def _get_temporal_label(label_options: dict[str, str], label_in: str, default: str) -> str:
    out_label = default

    for label, translation in label_options.items():
        if label in label_in:
            out_label = translation

    return out_label


def _get_vertical_label(label_options: dict[tuple, str], label_in: str, default: str) -> str:
    # sorts labels from longest to shortest
    sorted_labels = sorted(label_options.items(), key=lambda x: len(x[0]), reverse=True)

    for label, translation in sorted_labels:
        if label in label_in:
            
            # stops the loop as soon as a first match is found and returns match
            return translation
            
    # if no match is found, returns default        
    return default

    
def _get_horizontal_label(label_options: dict[tuple, str], label_in: str, default: str) -> str:

    for label_tuple, translation in label_options.items():
        if all(word in label_in for word in label_tuple):
            return translation

    return default



def _get_area_label(label_options: dict[tuple, str], label_in: str, default: str) -> str:
    out_label = default

    # sorts labels from longest to shortest
    sorted_labels = sorted(label_options.items(), key=lambda x: len(x[0]), reverse=True)

    for label, translation in sorted_labels:
        if label in label_in:
            
            # stops the loop as soon as a first match is found and returns match
            return translation
            
    # if no match is found, returns default        
    return default


def cmip_branded_variable_mapper(
    variable_name: str, cell_methods: str | None, dimensions: str
) -> str:
    """
    Map old CMIP variable information into branded variables

    Parameters
    ----------
    variable_name
        Variable name

    cell_methods
        Cell methods

    dimensions
        Dimensions

    Returns
    -------
    :
        Branded variable
    """
    if cell_methods is None:
        cell_methods = ""

    if (
        "time: max" not in cell_methods
        and "time: min" not in cell_methods
        and "time: sum" not in cell_methods
    ):
        temporalLabelDD = _get_temporal_label(time_labels_dimensions, dimensions, "ti")

    else:
        temporalLabelDD = _get_temporal_label(time_labels_cell_methods, cell_methods, "ti")

    verticalLabelDD = _get_vertical_label(vertical_labels, dimensions, "z0")

    horizontalLabelDD = _get_horizontal_label(horizontal_labels, dimensions, "hm")

    areaLabelDD = _get_area_label(area_labels, cell_methods, "x")

    suffix = "-".join(
        [temporalLabelDD, verticalLabelDD, horizontalLabelDD, areaLabelDD]
    )

    return "_".join([variable_name, suffix])
