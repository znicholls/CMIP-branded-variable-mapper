"""
Determination of the temporal label
"""

from __future__ import annotations

from cmip_branded_variable_mapper.mappers import CellMethodsSubStringMapper

TEMPORAL_LABEL_CELL_METHODS_MAPPER = CellMethodsSubStringMapper(
    sub_string_map={
        # TODO: switch to the below based on updates to the paper
        # "time: max": "tmax",
        # "time: min": "tmin",
        "time: max": "tstat",
        "time: min": "tstat",
        "time: sum": "tsum",
    }
)


def get_temporal_label(
    cell_methods: str | None,
    dimensions: tuple[str, ...],
    cell_methods_mapper: CellMethodsSubStringMapper = (
        TEMPORAL_LABEL_CELL_METHODS_MAPPER
    ),
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

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Temporal label to use for constructing the branded variable name
    """
    # Check cell methods first
    match = cell_methods_mapper.get_value(cell_methods)
    if match is not None:
        return match

    dimensions_labels = (
        ("time", "tavg"),
        ("time1", "tpt"),
        ("time2", "tclm"),
        ("time3", "tclmdc"),
    )
    for dimension, temporal_label in dimensions_labels:
        if dimension in dimensions:
            return temporal_label

    # Reproduce bug in existing implementation
    if "time" in " ".join(dimensions):
        return "tavg"

    return fallback
