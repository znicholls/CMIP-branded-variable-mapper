# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
"""
Regression tests of our branded variable mapper
"""

# %%
from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


# %%
def test_map_to_cmip_branded_variable_mapper(data_regression):
    branded_variable = map_to_cmip_branded_variable(
        variable_name="tas",
        cell_methods="mean where air",
        dimensions=("time", "lat", "lon"),
    )

    reg_check = {
        "variable_names": "tas",
        "cell_methods": "mean where air",
        "dimensions": ("time", "lat", "lon"),
        "branded_variable": branded_variable,
    }

    data_regression.check(reg_check)


# %%
