"""
Determination of the horizontal label
"""

from __future__ import annotations


def get_horizontal_label(
    dimensions: tuple[str, ...],
    fallback: str = "hm",
) -> str:
    """
    Get horizontal label

    The logic this should follow is defined in Table F3 of
    [Taylor et al.](https://docs.google.com/document/d/19jzecgymgiiEsTDzaaqeLP6pTvLT-NzCMaq-wu-QoOc/edit?pli=1&tab=t.0).
    This was last checked on September 24 2025.
    If updates have been made since,
    this code may be out of date with the underlying specification.

    Parameters
    ----------
    dimensions
        Dimensions of the variable

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        horizontal label to use for constructing the branded variable name
    """
    # The logic of Table F3 is pretty hard to follow
    # so we've gone for a verbose, but extremely clear implementation below
    # rather than trying to do something fancier.
    longitude_present = "longitude" in dimensions
    latitude_present = "latitude" in dimensions
    if (
        (longitude_present and latitude_present)
        or ("xant" in dimensions and "yant" in dimensions)
        or ("xgre" in dimensions and "ygre" in dimensions)
    ):
        return "hxy"

    basin_present = "basin" in dimensions
    if latitude_present and not (longitude_present or basin_present):
        return "hy"

    if "site" in dimensions:
        return "hs"

    if latitude_present and basin_present:
        return "hyb"

    if (
        "oline" in dimensions
        or "siline" in dimensions
        or ("gridlatitude" in dimensions and basin_present)
    ):
        return "ht"

    return fallback
