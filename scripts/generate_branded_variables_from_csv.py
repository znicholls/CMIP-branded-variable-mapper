from pathlib import Path
import pandas as pd
import numpy as np
import os

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


DATA_DIR = Path(__file__).parents[1] / "data"

df = pd.read_csv(DATA_DIR / Path("CMIP7-variables-for-branding.csv"))

df['CMIP7_branded_variable_name'] = df.apply(lambda row: map_to_cmip_branded_variable(row["Physical Parameter"], row["Cell Methods"], row["Dimensions"]), axis=1)

df.to_csv(DATA_DIR / Path("output/CMIP7-variables-with-branding.csv"))