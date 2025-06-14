"""
Determination of the temporal label
"""

from __future__ import annotations


def get_temporal_label(
    cell_methods: str | None,
    dimensions: tuple[str, ...],
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

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Temporal label to use for constructing the branded variable name
    """
    # Check cell methods first
    cell_methods_ids = (
        # TODO: switch to the below based on updates to the paper
        # ("time: max", "tmax"),
        # ("time: min", "tmin"),
        ("time: max", "tstat"),
        ("time: min", "tstat"),
        ("time: sum", "tsum"),
    )
    match: str | None = None
    for key_string, temporal_label in cell_methods_ids:
        if key_string in cell_methods:
            if match is None:
                match = temporal_label
            else:
                # Raise an error if we get multiple matches,
                # this should be impossible.
                msg = (
                    f"For {cell_methods=}, there are multiple matches. "
                    f"We already have {match=}, but {key_string} also matches "
                    f"(which would give a match of {temporal_label})"
                )
                raise AssertionError(msg)

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
