# %%
from pathlib import Path
import pandas as pd
import numpy as np
from contextlib import nullcontext as does_not_raise
import pytest
import tabulate

from cmip_branded_variable_mapper.mapper_old import cmip_branded_variable_mapper
from cmip_branded_variable_mapper.constants import (
    DATA_ROOT
)

# %%
df = pd.read_excel(DATA_ROOT / Path("CMIP6_branded_variables.xlsx"))
df = df.loc[:, ["variable registry root names", "new cell_methods",
                         "corrected CMIP6 dimensions", "proposed branded variable label"]].iloc[:2062]
df

# %%
expected = []
matching = []

for r in df.to_dict(orient="records"):
    expected.append(cmip_branded_variable_mapper(r["variable registry root names"],r["new cell_methods"],r["corrected CMIP6 dimensions"])
        )
    matching.append(expected[-1] == r["proposed branded variable label"]
                   )

df['expected'] = expected
df['matching'] = matching

# %%
df.columns = ["variable_names", "cell_methods", "dimensions", "branded_label-spreadsheet", "branded_label-following_spreadsheet", "matching"]
df

# %%
df.to_csv(DATA_ROOT / Path("compare_branded_variables-spreadsheet_definitions.csv"), index=False)
#df.to_csv(DATA_ROOT / Path("compare_branded_variables.csv"), index = False)

# %%
fails = df[df["matching"] == False]
fails

# %%
fails.to_csv(DATA_ROOT / Path("compare_branded_variables-spreadsheet_definitions-false.csv"), index=False)

# %%
print(fails.to_markdown(index=False))

# %%
#df[df["branded_label-spreadsheet"] == df["branded_label-following_appendixF"]]
df[df["branded_label-spreadsheet"] == df["branded_label-following_spreadsheet"]]

# %%
for row in df_filtered.T:
    #print(df_filtered.iloc[row]["proposed branded variable label"].split("_")[0])
    try:
        if df_filtered.iloc[row]["variable registry root names"] != df_filtered.iloc[row]["proposed branded variable label"].split("_")[0]:
            print(df_filtered.iloc[row]["variable registry root names"], df_filtered.iloc[row]["proposed branded variable label"])
    except:
        print(row)


# %%
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
#print(generate_expected_cases())


# %%
@generate_expected_cases()
def test_against_excel_sheet(variable_name, cell_methods, dimensions, exp):
    
    assert cmip_branded_variable_mapper(variable_name, cell_methods, dimensions) == exp, "Beschwerde eingereicht"


# %%
data_file = DATA_ROOT / Path("CMIP6_branded_variables.xlsx")
#df = pd.read_excel(data_file)


def _get_label(label_options: dict, label_in: str, default: str) -> str:
    
    out_label = default
    
    for label,translation in label_options.items():
            if label in label_in:
                out_label = f"{translation}"
    
    return out_label
    

def cmip_branded_variable_mapper(variable_name: str, cell_methods:str, dimensions:str) -> str:
    
    """
    Constructs a CMIP7 branded variable name based on variable metadata from CMIP6.
    
    Args:
        variable_name: Name of the variable in CMIP6 and CMIP7
        cell_methods: Cell methods string containing processing information
        dimensions: Dimensions string containing variable dimensions
        
    Returns: CMIP7 branded variable name 
        
    """
    
    if "time" in dimensions: 
        
        temporalLabelDD = _get_label(time_labels_dimensions, dimensions, 'ti')
        
    else: 
        
        temporalLabelDD = _get_label(time_labels_cell_methods, cell_methods, 'ti')
        
    verticalLabelDD = _get_label(vertical_labels, dimensions, 'u')

    horizontalLabelDD = _get_label(horizontal_labels, dimensions, 'hm')

    areaLabelDD = _get_label(area_labels, cell_methods, 'u')
            
    return f"{variable_name}_{temporalLabelDD}-{verticalLabelDD}-{horizontalLabelDD}-{areaLabelDD}"


# %%
cmip_branded_variable_mapper("ares", "area: mean where land time: rudolf", "longitude latitude penny")

# %%
ares_tavg-z0-hxy-lnd
