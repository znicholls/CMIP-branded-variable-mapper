"""
Mapper from CMIP information to branded variables

In the absence of other references,
this is currently our source of truth for this mapping.
(https://docs.google.com/document/d/149Tkz37whSQMFVbEYZMYbdqIctHbufpbJ_VMlzHyKuY/edit?tab=t.0).
"""

from __future__ import annotations

from cmip_branded_variable_mapper.temporal_label import get_temporal_label
from cmip_branded_variable_mapper.vertical_label import get_vertical_label

vertical_labels = {
    "sdepth": "l",
    "olevel": "l",
    "alevel": "l",
    "alevhalf": "l",
    "olevhalf": "l",
    "rho": "rho",
    "height2m": "h2m",
    "height10m": "h10m",
    "height100m": "h100m",
    "sdepth1": "d10cm",
    "sdepth10": "d100cm",
    "depth0m": "d0m",
    "depth100m": "d100m",
    "depth300m": "d300m",
    "depth700m": "d700m",
    "depth1000m": "d1000m",
    "depth2000m": "d2000m",
    "olayer100m": "d100m",
    "olayer300m": "d300m",
    "olayer700m": "d700m",
    "olayer2000m": "d2000m",
    "op20bar": "op20bar",
    "p10": "10hPa",
    "p100": "100hPa",
    "p200": "200hPa",
    "p220": "220hPa",
    "p500": "500hPa",
    "p560": "560hPa",
    "p700": "700hPa",
    "pl700": "700hPa",
    "p840": "840hPa",
    "p850": "850hPa",
    "p925": "925hPa",
    "p1000": "1000hPa",
    "alt16": "h16",
    "alt40": "h40",
    "plev3": "p3",
    "plev4": "p4",
    "plev5u": "p5u",
    "plev6": "p6",
    "plev8": "p8",
    "plev7c": "p7c",
    "plev7h": "p7h",
    "plev19": "p19",
    "plev27": "p27",
    "plev39": "p39",
    "oplev4": "op4",
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
    "where sector": "multi",
    "where shrubs": "shb",
    "where snow": "sn",
    "where stratiform_cloud": "scl",
    "where trees": "tree",
    "where unfrozen_soil": "ufs",
    "where vegetation": "veg",
    "where wetland": "wl",
}


def _get_vertical_label(
    label_options: dict[str, str], label_in: tuple[str, ...], default: str
) -> str:
    # sorts labels from longest to shortest
    sorted_labels = sorted(label_options.items(), key=lambda x: len(x[0]), reverse=True)

    for label, translation in sorted_labels:
        if label in label_in:
            # stops the loop as soon as a first match is found and returns match
            return translation

    # if no match is found, returns default
    return default


def _get_horizontal_label(
    label_options: dict[tuple[str, ...], str], label_in: tuple[str, ...], default: str
) -> str:
    for label_tuple, translation in label_options.items():
        if all(word in label_in for word in label_tuple):
            return translation

    return default


def _get_area_label(label_options: dict[str, str], label_in: str, default: str) -> str:
    # sorts labels from longest to shortest
    sorted_labels = sorted(label_options.items(), key=lambda x: len(x[0]), reverse=True)

    for label, translation in sorted_labels:
        if label in label_in:
            # stops the loop as soon as a first match is found and returns match
            return translation

    # if no match is found, returns default
    return default


def map_to_cmip_branded_variable(
    variable_name: str, cell_methods: str | None, dimensions: tuple[str, ...]
) -> str:
    """
    Map CMIP variable information into a branded variable

    Parameters
    ----------
    variable_name
        Variable name

    cell_methods
        Cell methods associated with the variable

    dimensions
        Dimensions of the variable

    Returns
    -------
    :
        Branded variable

    Examples
    --------
    >>> map_to_cmip_branded_variable(
    ...     variable_name="tas",
    ...     cell_methods="area: time: mean",
    ...     dimensions=("longitude", "latitude", "time", "height2m"),
    ... )
    'tas_tavg-h2m-hxy-u'
    >>>
    >>> map_to_cmip_branded_variable(
    ...     variable_name="hfds",
    ...     cell_methods="area: mean where sea time: mean",
    ...     dimensions=("longitude", "latitude", "time"),
    ... )
    'hfds_tavg-u-hxy-sea'
    """
    temporal_label = get_temporal_label(
        cell_methods=cell_methods, dimensions=dimensions
    )

    vertical_label = get_vertical_label(dimensions=dimensions)

    if cell_methods is None:
        cell_methods = ""

    horizontalLabelDD = _get_horizontal_label(horizontal_labels, dimensions, "hm")

    areaLabelDD = _get_area_label(area_labels, cell_methods, "u")

    suffix = "-".join([temporal_label, vertical_label, horizontalLabelDD, areaLabelDD])

    return "_".join([variable_name, suffix])
