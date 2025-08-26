"""
Determination of the area label
"""

from __future__ import annotations

from cmip_branded_variable_mapper.mapper_classes import (
    CellMethodsSubStringMapperOrdered,
)

AREA_LABEL_CELL_METHODS_MAPPER = CellMethodsSubStringMapperOrdered.from_unordered(
    {
        "area: mean (over land and sea ice)": "lsi",
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
)
"""
Mapper from sub-strings of cell methods to the area label
"""


def get_area_label(
    cell_methods: str | None,
    cell_methods_mapper: CellMethodsSubStringMapperOrdered = (
        AREA_LABEL_CELL_METHODS_MAPPER
    ),
    fallback: str = "u",
) -> str:
    """
    Get area label

    The logic this should follow is defined in Table F4 of
    [Taylor et al.](https://docs.google.com/document/d/19jzecgymgiiEsTDzaaqeLP6pTvLT-NzCMaq-wu-QoOc/edit?pli=1&tab=t.0).
    This was last checked on June 14 2025.
    If updates have been made since,
    this code may be out of date with the underlying specification.

    Parameters
    ----------
    cell_methods
        Cell methods of the variable

    cell_methods_mapper
        Mapper to use to get values based on cell methods

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Area label to use for constructing the branded variable name
    """
    if cell_methods is not None:
        if (match := cell_methods_mapper.get_value(cell_methods)) is not None:
            return match

    return fallback
