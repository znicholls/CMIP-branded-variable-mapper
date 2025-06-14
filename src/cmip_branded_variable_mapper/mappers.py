"""
Tools for mapping from variable information to branded variable components

Custom as the mapping needs to be careful to avoid accidental clashes.
"""

from __future__ import annotations

import itertools
from typing import Any

import attr
from attrs import define, field


@define
class CellMethodsSubStringMapper:
    """
    Mapper that returns values based on matches of sub-strings in cell methods
    """

    sub_string_map: dict[str, str] = field()
    """
    Map from sub-strings of cell methods to the metadata value to use
    """

    @sub_string_map.validator
    def sub_string_map_validator(
        self,
        attribute: attr.Attribute[Any],
        value: dict[str, str],
    ) -> None:
        """
        Validate the received map

        The key here is that the keys can't lead to accidental clashes
        """
        for k1, k2 in itertools.permutations(value.keys(), r=2):
            if k1 in k2:
                msg = (
                    f"{k1!r} is a subset of {k2!r}. "
                    "You will need a different mapper or keys "
                    "to avoid incorrect results."
                )
                raise AssertionError(msg)

    def get_value(self, cell_methods: str) -> str | None:
        """
        Get the metadata value for a given value of cell_methods

        Parameters
        ----------
        cell_methods
            Cell methods

        Returns
        -------
        :
            Metadata value.

            If no matches are found, `None` is returned.
        """
        for sub_string, value in self.sub_string_map.items():
            if sub_string in cell_methods:
                return value

        return None


@define
class DimensionMapper:
    """
    Mapper that returns values based on whether dimensions are present or not
    """

    dimension_map: dict[str, str]
    """
    Map from dimensions to the metadata value to use
    """

    def get_value(self, dimensions: tuple[str, ...]) -> str | None:
        """
        Get the metadata value for a given value of dimensions

        Parameters
        ----------
        dimensions
            Dimensions to check

        Returns
        -------
        :
            Metadata value.

            If no matches are found, `None` is returned.
        """
        for dimension, value in self.dimension_map.items():
            if dimension in dimensions:
                return value

        return None
