# %%
"""
Tests of our generation of branded variable names
"""

# %% [markdown]
# Tests to write:
# - Given a CMIP6 variable name and cell methods, do we get expected output
# - Match the behaviour specified in the excel table
# - Given a branded variable, get back to CMIP6 variable and cell methods
# - Round tripping
# - If you give an uncreognised name, you get a sensible error

# %%
from contextlib import nullcontext as does_not_raise
from pathlib import Path

# %%
import pandas as pd
import pytest

# %%
HERE = Path(__file__).parent


# %%
def generate_expected_cases():
    raw = pd.read_csv(HERE / "expected-mappings.csv")

    exp_var_names = ["variable", "cell_methods", "exp"]
    col_names = ["variable", "cell_methods", "branded_variable"]
    test_cases = [
        pytest.param(*[r[ov] for ov in col_names])
        for r in raw.to_dict(orient="records")
    ]

    return pytest.mark.parametrize(exp_var_names, test_cases)


# %%
@generate_expected_cases()
def test_against_excel_sheet(variable, cell_methods, exp):
    assert False


# %%
@pytest.mark.parametrize(
    ["variable", "cell_methods", "exp"],
    (
        pytest.param(
            "tas", "time: mean area: mean", "tas-tavg-hx-u-u", id="tas-average"
        ),
        ("hfds", "time: mean area: sum", "hfds-tavg-hx-s-u"),
        ("junk", "time: mean area: sum", "hfds-tavg-hx-s-u"),
    ),
)
def test_basic(variable, cell_methods, exp):
    res = get_branded_variable(variable=variable, cell_methods=cell_methods)

    assert res == exp


# %%
@pytest.mark.parametrize(
    ["variable", "expectation"],
    (
        pytest.param("tas", does_not_raise()),
        pytest.param(
            "junk", pytest.raises(KeyError, match="some helpful error message here")
        ),
    ),
)
def test_unrecognised_variable_raises(variable, expectation):
    with expectation:
        get_branded_variable(variable=variable, cell_methods="not used")
