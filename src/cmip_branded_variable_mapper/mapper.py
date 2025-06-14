"""
Mapper from CMIP information to branded variables

In the absence of other references,
this is currently our source of truth for this mapping.
(https://docs.google.com/document/d/149Tkz37whSQMFVbEYZMYbdqIctHbufpbJ_VMlzHyKuY/edit?tab=t.0).
"""

from __future__ import annotations

from cmip_branded_variable_mapper.area_label import get_area_label
from cmip_branded_variable_mapper.horizontal_label import get_horizontal_label
from cmip_branded_variable_mapper.temporal_label import get_temporal_label
from cmip_branded_variable_mapper.vertical_label import get_vertical_label


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
    area_label = get_area_label(cell_methods=cell_methods)

    suffix = "-".join([temporal_label, vertical_label, horizontal_label, area_label])

    return "_".join([variable_name, suffix])
