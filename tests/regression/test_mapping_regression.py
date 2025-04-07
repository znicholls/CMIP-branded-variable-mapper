"""
Regression tests of our mapping to branded variables
"""

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


def test_map_to_branded_variables(data_regression):
    branded_variable = map_to_cmip_branded_variable(
        variable_name="tas",
        cell_methods="mean where air",
        dimensions=("time", "lat", "lon"),
    )
    reg_check = {
        "variable_name": "tas",
        "cell_methods": "mean where air",
        "dimensions": ("time", "lat", "lon"),
        "branded_variable": branded_variable,
    }
    data_regression.check(reg_check)
