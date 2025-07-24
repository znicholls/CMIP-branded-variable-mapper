"""
Determination of the vertical label
"""

from __future__ import annotations

from cmip_branded_variable_mapper.mapper_classes import DimensionMapper

VERTICAL_LABEL_DIMENSIONS_MAPPER = DimensionMapper(
    dimension_map={
        "sdepth": "sl",
        "olevel": "ol",
        "alevel": "al",
        "alevhalf": "alh",
        "olevhalf": "olh",
        "rho": "rho",
        "height2m": "h2m",
        "height10m": "h10m",
        "height100m": "h100m",
        "sdepth10cm": "d10cm",
        "sdepth100cm": "d100cm",
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
        "oplayer4": "op4",
    }
)
"""
Mapper from dimensions to the vertical label
"""


def get_vertical_label(
    dimensions: tuple[str, ...],
    dimensions_mapper: DimensionMapper = VERTICAL_LABEL_DIMENSIONS_MAPPER,
    fallback: str = "u",
) -> str:
    """
    Get vertical label

    The logic this should follow is defined in Table F2 of
    [Taylor et al.](https://docs.google.com/document/d/19jzecgymgiiEsTDzaaqeLP6pTvLT-NzCMaq-wu-QoOc/edit?pli=1&tab=t.0).
    This was last checked on June 14 2025.
    If updates have been made since,
    this code may be out of date with the underlying specification.

    Parameters
    ----------
    dimensions
        Dimensions of the variable

    dimensions_mapper
        Mapper to use to get values based on dimensions

    fallback
        Value to return if no other conditions are matched

    Returns
    -------
    :
        Vertical label to use for constructing the branded variable name
    """
    if (match := dimensions_mapper.get_value(dimensions)) is not None:
        return match

    return fallback
