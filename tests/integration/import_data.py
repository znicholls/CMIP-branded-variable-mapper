# %%
from pathlib import Path
import pandas as pd
import numpy as np

from cmip_branded_variable_mapper.constants import (
    DATA_ROOT
)

# %%
data_folder = DATA_ROOT

# %%
data_file = DATA_ROOT / Path("CMIP6_branded_variables.xlsx")

# %%
df = pd.read_excel(data_file)

# %%
# variable name: column BY "variable registry root names"
# cell methods: column T "new cell_methods"
# dimensions: column AZ "corrected CMIP6 dimensions"

# branded variable name: column BK "proposed branded variable label"

# %%
# filter only variables we need and drop NAs
# we can probably delete this step later on, but for now it just makes it a bit easier to follow what is happening

df_filtered = df.loc[:, ["variable registry root names", "new cell_methods", 
                         "corrected CMIP6 dimensions", "proposed branded variable label"]].iloc[:2062]

# %%
df_filtered

# %%
for row in df_filtered.T:
    #print(df_filtered.iloc[row]["proposed branded variable label"].split("_")[0])
    try:
        if df_filtered.iloc[row]["variable registry root names"] != df_filtered.iloc[row]["proposed branded variable label"].split("_")[0]:
            print(df_filtered.iloc[row]["variable registry root names"], df_filtered.iloc[row]["proposed branded variable label"])
    except:
        print(row)

# %% [markdown]
# construction methods:
# rootname_time-vertical_label-horizontal_label-masking
#
#
# for time either
# in cell_methods:
# time: mean --> tavg
# time : point --> tpt
# time: max --> tstat
# time: min --> tstat
# time: sum --> tsum
#
# or in dimensions:
# time --> tavg
# time1 --> tpt
# time2 --> tclm
# time3 --> tclmdc
#

# %%
time_labels_dimensions = {
    "time": "tavg",
    "time1": "tpt",
    "time2": "tclm",
    "time3": "tclmdc"
}

# %%
time_labels_cell_methods = {
    "time: max": "tstat",
    "time: min": "tstat",
    "time: sum": "tsum"
}

# %%
vertical_labels = {
    "sdepth": "l",
    "olevel": "l",
    "alevel": "l",
    "alevhalf": "l",
    "olevhalf": "l",
    "rho": "rho",
    "height2m": "h2m",
    "height10m": "h10m",
    "height100m": "h100m",
    "sdepth1": "d10cm",
    "sdepth10": "d1m",
    "depth0m": "d0m",
    "depth100m": "d100m",
    "olayer100m": "d100m",
    "olayer300m": "d300m",
    "olayer700m": "d700m",
    "olayer2000m": "d2000m",
    "p10": "10hPa",
    "p100": "100hPa",
    "p220": "220hPa",
    "p500": "500hPa",
    "p560": "560hPa",
    "p700": "700hPa",
    "pl700": "700hPa",
    "p840": "840hPa",
    "p850": "850hPa",
    "p1000": "1000hPa",
    "alt16": "h16",
    "alt40": "h40",
    "plev3": "p3",
    "plev4": "p4",
    "plev8": "p8",
    "plev7c": "p7c",
    "plev7h": "p7h",
    "plev19": "p19",
    "plev27": "p27",
    "plev39": "p39"
}


# %%
horizontal_labels = {
    "latitude": "hy",
    "longitude latitude": "hxy",
    "xant yant": "hxy",
    "xgre ygre": "hxy",
    "site": "hxys",
    "latitude basin": "hys",
    "gridlatitude basin": "ht",
    "oline": "ht",
    "siline": "ht"
}

# %%
area_labels = {
    "air": "air",
    "cloud": "cl",
    "convective_cloud": "ccl",
    "crops": "crp",
    "floating_ice_shelf": "fis",
    "grounded_ice_sheet": "gis",
    "ice_free_sea": "ifs",
    "ice_sheet": "is",
    "land": "lnd",
    "land_ice": "li",
    "natural_grasses": "ng",
    "pastures": "pst",
    "sea": "sea",
    "sea_ice": "si",
    "sea_ice_melt_pond": "simp",
    "sea_ice_ridges": "sir",
    "sector": "lus",
    "shrubs": "shb",
    "snow": "sn",
    "stratiform_cloud": "scl",
    "trees": "tree",
    "unfrozen_soil": "ufs",
    "vegetation": "veg",
    "wetland": "wl"
}

# %%
data_file = DATA_ROOT / Path("CMIP6_branded_variables.xlsx")
df = pd.read_excel(data_file)

def cmip_branded_variable_mapper(variable_name: str, cell_methods:str, dimensions:str) -> str:

    temporalLabelDD = "-ti"
    

    verticalLabelDD = "-u"
    
    for vertical_label,translation in vertical_labels.items():
        if vertical_label in dimensions:
            verticalLabelDD = f"-{translation}"

    horizontalLabelDD = "-hm"
    
    for horizontal_label,translation in horizontal_labels.items():
        if horizontal_label in dimensions:
            horizontalLabelDD = f"-{translation}"

    areaLabelDD = "-u"
    
    for area_label,translation in area_labels.items():
        if f"where {area_label}" in cell_methods:
            areaLabelDD = f"-{translation}"
            
    return f"{variable_name}_{temporalLabelDD}{verticalLabelDD}{horizontalLabelDD}{areaLabelDD}"

