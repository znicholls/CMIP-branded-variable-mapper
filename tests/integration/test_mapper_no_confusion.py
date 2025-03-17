"""
Tests of our mapping from old names to branded variables
"""

from pathlib import Path

import pandas as pd
import pytest

from cmip_branded_variable_mapper.mapper_old import cmip_branded_variable_mapper

DATA_DIR = Path(__file__).parents[2] / "data"


def generate_expected_cases():
    df = pd.read_excel(DATA_DIR / Path("CMIP6_branded_variables.xlsx"))
    df = df.loc[
        :,
        [
            "variable registry root names",
            "new cell_methods",
            "corrected CMIP6 dimensions",
            "proposed branded variable label",
        ],
    ]
    df = df[
        ~df["proposed branded variable label"].isnull()
        & ~df["proposed branded variable label"].str.contains(":").astype(bool)
        & ~(
            df["proposed branded variable label"]
            .str.contains("proposed branded variable label")
            .astype(bool)
        )
    ]

    exp_var_names = ["variable_name", "cell_methods", "dimensions", "exp"]
    col_names = [
        "variable registry root names",
        "new cell_methods",
        "corrected CMIP6 dimensions",
        "proposed branded variable label",
    ]
    test_cases = []
    for record in df.to_dict(orient="records"):
        # Replace all NaN cell methods with None
        param_values = [
            record[ov] if not pd.isnull(record[ov]) else None for ov in col_names
        ]

        test_cases.append(pytest.param(*param_values))

    return pytest.mark.parametrize(exp_var_names, test_cases)


@generate_expected_cases()
def test_against_excel_sheet(variable_name, cell_methods, dimensions, exp):
    assert (
        cmip_branded_variable_mapper(variable_name, cell_methods, dimensions) == exp
    ), f"Got {cmip_branded_variable_mapper(variable_name, cell_methods, dimensions)} expected {exp}"  # noqa: E501
