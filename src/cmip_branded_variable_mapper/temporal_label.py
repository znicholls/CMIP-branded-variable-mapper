"""
Determination of the temporal label
"""

from __future__ import annotations

from cmip_branded_variable_mapper.mapper_classes import (
    CellMethodsSubStringMapper,
    DimensionMapper,
)

TEMPORAL_LABEL_CELL_METHODS_MAPPER = CellMethodsSubStringMapper(
    sub_string_map={
        "time: max": "tmax",
        "time: min": "tmin",
        "time: sum": "tsum",
    }
)
"""
Mapper from sub-strings of cell methods to the temporal label
"""

TEMPORAL_LABEL_DIMENSIONS_MAPPER = DimensionMapper(
    dimension_map={
        "time": "tavg",
        "time1": "tpt",
        "time2": "tclm",
        "time3": "tclmdc",
    }
)
"""
Mapper from dimensions to the temporal label
"""


def get_temporal_label(
    cell_methods: str | None,
    dimensions: tuple[str, ...],
    cell_methods_mapper: CellMethodsSubStringMapper = (
        TEMPORAL_LABEL_CELL_METHODS_MAPPER
    ),
    dimensions_mapper: DimensionMapper = TEMPORAL_LABEL_DIMENSIONS_MAPPER,
    fallback: str = "ti",
) -> str:
    """
    Get temporal label

    The logic this should follow is defined in Table F1 of
    [Taylor et al.](https://docs.google.com/document/d/19jzecgymgiiEsTDzaaqeLP6pTvLT-NzCMaq-wu-QoOc/edit?pli=1&tab=t.0).
    This was last checked on June 14 2025.
    If updates have been made since,
    this code may be out of date with the underlying specification.

    Parameters
    ----------
    cell_methods
        Cell methods of the variable

    dimensions
        Dimensions of the variable

    cell_methods_mapper
        Mapper to use to get values based on cell methods

    dimensions_mapper
        Mapper to use to get values based on dimensions

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Temporal label to use for constructing the branded variable name
    """
    if cell_methods is not None:
        # Check cell methods first
        if (match := cell_methods_mapper.get_value(cell_methods)) is not None:
            return match

    if (match := dimensions_mapper.get_value(dimensions)) is not None:
        return match

    return fallback
