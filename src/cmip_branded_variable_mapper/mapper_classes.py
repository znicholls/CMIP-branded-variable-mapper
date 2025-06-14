"""
Classes for mapping from variable information to branded variable components

These have a custom implementation
because there is a coupling between the mapping and the matching algorithms
(and the classes ensure that this coupling is respected).
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


@define
class CellMethodsSubStringMapperOrdered:
    """
    Mapper that returns values based on matches of ordered sub-strings in cell methods

    The ordering matters because it ensures
    that we don't get accidental clashes
    by checking for the longest possible match first.
    """

    sub_string_map: tuple[tuple[str, str], ...] = field()
    """
    Map from sub-strings of cell methods to the metadata value to use

    The first element of each tuple is the sub-string to check for matches,
    the second element is the metadata value to use if this sub-string is a match.

    These must be provide as a tuple of tuples to ensure that the ordering is preserved.
    """

    @sub_string_map.validator
    def sub_string_map_validator(
        self,
        attribute: attr.Attribute[Any],
        value: tuple[tuple[str, str], ...],
    ) -> None:
        """
        Validate the received map

        The key here is that the keys can't lead to accidental clashes
        """
        for i, v in enumerate(value[::-1]):
            # Keys always checked in order,
            # so we only need to check keys that come before this one.
            check_until = len(value) - i - 1
            for v_potential_clash in value[:check_until]:
                if v_potential_clash[0] in v[0]:
                    msg = (
                        f"{v_potential_clash[0]!r} is a subset of {v[0]!r}. "
                        "You will need to re-order your mapper "
                        "to avoid incorrect results."
                    )
                    raise AssertionError(msg)

    @classmethod
    def from_unordered(
        cls, unordered_map: dict[str, str]
    ) -> CellMethodsSubStringMapperOrdered:
        """
        Initialise from an unordered map

        Parameters
        ----------
        unordered_map
            Unordered map

        Returns
        -------
        :
            Initialised instance
        """
        sub_string_map = tuple(
            (key, unordered_map[key])
            for key in sorted(unordered_map.keys(), key=len, reverse=True)
        )

        return cls(sub_string_map=sub_string_map)

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
        for sub_string, value in self.sub_string_map:
            if sub_string in cell_methods:
                return value

        return None
