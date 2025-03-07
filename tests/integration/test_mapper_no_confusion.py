from pathlib import Path
import pandas as pd
import numpy as np
from contextlib import nullcontext as does_not_raise
import pytest

from cmip_branded_variable_mapper.mapper_old import cmip_branded_variable_mapper
from cmip_branded_variable_mapper.constants import (
    DATA_ROOT
)

# test for mapper using last year's definitions from the spreadsheet

def generate_expected_cases():
    
    df = pd.read_excel(DATA_ROOT / Path("CMIP6_branded_variables.xlsx"))
    df = df.loc[:, ["variable registry root names", "new cell_methods",
                         "corrected CMIP6 dimensions", "proposed branded variable label"]].iloc[:2062]
    
    exp_var_names = ["variable_name", "cell_methods", "dimensions", "exp"]
    col_names = ["variable registry root names", "new cell_methods",
                         "corrected CMIP6 dimensions", "proposed branded variable label"]
    test_cases = [
        pytest.param(*[r[ov] for ov in col_names])
        for r in df.to_dict(orient="records")
    ]

    return pytest.mark.parametrize(exp_var_names, test_cases)


@generate_expected_cases()
def test_against_excel_sheet(variable_name, cell_methods, dimensions, exp):
    
    assert cmip_branded_variable_mapper(variable_name, cell_methods, dimensions) == exp, f"Got {cmip_branded_variable_mapper(variable_name, cell_methods, dimensions)} expected {exp}"