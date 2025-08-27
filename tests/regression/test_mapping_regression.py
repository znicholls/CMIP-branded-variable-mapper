"""
Regression tests of our branded variable mapper
"""

from pathlib import Path

import pandas as pd

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable

HERE = Path(__file__).parent


def test_map_to_cmip_branded_variable_mapper(data_regression):
    # TODO: switch to using variable registry
    # https://github.com/WCRP-CMIP/Variable-Registry
    TEST_CASES_FILE = HERE.parent / "test-data" / "CMIP7-variables-for-branding.csv"

    raw_test_cases = pd.read_csv(TEST_CASES_FILE)

    res_l = []
    for _, row in raw_test_cases.iterrows():
        dimensions = tuple([v.strip() for v in row["Dimensions"].split(",")])
        variable_name = row["Physical Parameter"]
        cell_methods = (row["Cell Methods"],)

        branded_variable = map_to_cmip_branded_variable(
            variable_name=variable_name,
            cell_methods=cell_methods,
            dimensions=dimensions,
        )

        reg_check = {
            "variable_name": variable_name,
            "cell_methods": cell_methods,
            "dimensions": dimensions,
            "branded_variable": branded_variable,
        }

        res_l.append(reg_check)

    res_l.sort(key=lambda x: x["branded_variable"])
    data_regression.check(res_l)
