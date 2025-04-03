# create clean list of test cases
# - save as JSON
# - tests will load these test cases
# - run the test
# - save the output as regression output


from pathlib import Path

import pandas as pd

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable

TEST_DATA_DIR = Path(__file__).parents[1] / "test-data"


def generate_test_cases():
    df = pd.read_csv(TEST_DATA_DIR / "map-branded-variables-input.csv")

    for record in df.to_dict(orient="records"):
        variable_name = record["variable"]
        dimensions = tuple(v.strip() for v in record["dimensions"].split(","))
        cell_methods = record["cell_methods"]

        yield variable_name, cell_methods, dimensions


def test_map_to_cmip_branded_variable_regression(data_regression):
    res_l = []
    for variable_name, cell_methods, dimensions in generate_test_cases():
        branded_variable = map_to_cmip_branded_variable(
            variable_name=variable_name,
            dimensions=dimensions,
            cell_methods=cell_methods,
        )

        res = {
            "variable_name": variable_name,
            "dimensions": dimensions,
            "cell_methods": cell_methods,
            "branded_variable": branded_variable,
        }

        res_l.append(res)

    # Ensure order so we don't get failures because of ordering issues
    # as we add new test cases
    res_l.sort(key=lambda x: x["branded_variable"])

    data_regression.check(res_l)
