"""
Determination of the temporal label
"""

from __future__ import annotations

from cmip_branded_variable_mapper.mapper_classes import (
    CellMethodsSubStringMapper,
    DimensionMapper,
)

TEMPORAL_LABEL_CELL_METHODS_INITIAL_TESTS_MAPPER = CellMethodsSubStringMapper(
    sub_string_map={
        "time: max": "tmax",
        "time: min": "tmin",
        "time: sum": "tsum",
    }
)
"""
Mapper from sub-strings of cell methods to the temporal label

These are for the 'initial tests'
i.e. the cell methods which are checked first.
There is a coupling with dimensions in the logic in
[get_temporal_label][(m).], be careful!
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

TEMPORAL_LABEL_CELL_METHODS_TIME4_TESTS_MAPPER = CellMethodsSubStringMapper(
    sub_string_map={
        "time: max": "tmaxavg",
        "time: min": "tminavg",
    }
)
"""
Mapper from sub-strings of cell methods to the temporal label for "time4" data

I.e. for data which has "time4" as a dimension
"""


def get_temporal_label(  # noqa: PLR0913
    cell_methods: str | None,
    dimensions: tuple[str, ...],
    cell_methods_initial_mapper: CellMethodsSubStringMapper = (
        TEMPORAL_LABEL_CELL_METHODS_INITIAL_TESTS_MAPPER
    ),
    cell_methods_initial_required_dimension: str = "time",
    dimensions_mapper: DimensionMapper = TEMPORAL_LABEL_DIMENSIONS_MAPPER,
    cell_methods_time4_mapper: CellMethodsSubStringMapper = (
        TEMPORAL_LABEL_CELL_METHODS_TIME4_TESTS_MAPPER
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

    cell_methods_initial_mapper
        Mapper to use to get values based on cell methods

        This is for the 'initial' tests
        i.e. checks of cell methods which are performed
        before any other checks.

    cell_methods_initial_required_dimension
        Dimension required for the result of using `cell_methods_initial_mapper`
        to be returned.

        If this dimension is not found, then the other mapping checks are performed.

    dimensions_mapper
        Mapper to use to get values based on dimensions

        If you include "time4" as a mapping here,
        you can make a mess as you will effectively
        disable any use of `cell_methods_time4_mapper`.

    cell_methods_time4_mapper
        Mapper to use to get values based on cell methods if "time4" is in dimensions

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Temporal label to use for constructing the branded variable name
    """
    if cell_methods is not None:
        # Check cell methods first
        if (match := cell_methods_initial_mapper.get_value(cell_methods)) is not None:
            if cell_methods_initial_required_dimension in dimensions:
                return match

            # We matched cell methods but not the required dimension,
            # fall through to other tests

    if (match := dimensions_mapper.get_value(dimensions)) is not None:
        return match

    if cell_methods is not None and "time4" in dimensions:
        if (match := cell_methods_time4_mapper.get_value(cell_methods)) is not None:
            return match

    return fallback
