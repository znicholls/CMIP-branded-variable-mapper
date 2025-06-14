"""
Mapper from CMIP information to branded variables

In the absence of other references,
this is currently our source of truth for this mapping.
(https://docs.google.com/document/d/149Tkz37whSQMFVbEYZMYbdqIctHbufpbJ_VMlzHyKuY/edit?tab=t.0).
"""

from __future__ import annotations

from cmip_branded_variable_mapper.horizontal_label import get_horizontal_label
from cmip_branded_variable_mapper.temporal_label import get_temporal_label
from cmip_branded_variable_mapper.vertical_label import get_vertical_label

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
    horizontal_label = get_horizontal_label(dimensions=dimensions)

    if cell_methods is None:
        cell_methods = ""

    areaLabelDD = _get_area_label(area_labels, cell_methods, "u")

    suffix = "-".join([temporal_label, vertical_label, horizontal_label, areaLabelDD])

    return "_".join([variable_name, suffix])
