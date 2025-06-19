# ---
# jupyter:
#   jupytext:
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
from pathlib import Path

import pandas as pd

from cmip_branded_variable_mapper import map_to_cmip_branded_variable

# %%
pd.options.display.max_columns = 100

# %% [markdown]
# In order to run this, you will need to download the CSV from AirTable.
#
# To do this:
#
# 1. go to https://airtable.com/appBWxP0SS7K1hweJ/shrxhV6tenQBnOGRj/tblTLr91kMNaQTiCQ/viw82lb29IupSWCvv?blocks=hide
# 2. hit "MASTER" -> Download CSV
# 3. Save it somewhere
# 4. Update the path below to point to the right spot
#
# I have done this deliberately:
# we should be using the latest version on AirTable to avoid reporting
# things after they're changed.
# That means you might not get exactly the same results as someone else, so be it.

# %%
raw_dr = pd.read_csv(Path("20250619-1446_Variable-MASTER.csv"))
raw_dr.head(2)

# %%
# Not sure if this is quite correct for a filtered list, but probably near enough for round 1
raw_dr_not_rejected = raw_dr[raw_dr["Status"] != "Rejected"].copy()
raw_dr_not_rejected.shape


# %% [markdown]
# Question 1: does the algorithm work on all rows?


# %%
def get_branded_variable(row: pd.Series) -> str:
    variable_name = row["Physical Parameter"]
    dimensions = tuple(v.strip() for v in row["Dimensions"].split(", "))
    cell_methods = row["Cell Methods"]

    branded_variable = map_to_cmip_branded_variable(
        variable_name=variable_name,
        dimensions=dimensions,
        cell_methods=cell_methods,
    )

    return branded_variable


raw_dr_not_rejected["branded_variable"] = raw_dr_not_rejected[
    ["Physical Parameter", "Dimensions", "Cell Methods"]
].apply(get_branded_variable, axis="columns")
raw_dr_not_rejected

# %% [markdown]
# Answer: yes
#
# Conclusion: no issue from a pure 'does the code work point of view', carry on
# to checking content.

# %% [markdown]
# Question 2: Do we get duplicates?

# %%
dups = raw_dr_not_rejected[
    raw_dr_not_rejected["branded_variable"].duplicated(keep=False)
].sort_values("branded_variable")
dups

# %% [markdown]
# Answer: yes
#
# Conclusion: TBC - keep digging first

# %% [markdown]
# Question 3: How many are due to Greenland/Antarctica issues?

# %%
if raw_dr_not_rejected["CMIP6 Compound Name"].duplicated().any():
    raise AssertionError("This won't end well")

raw_dr_not_rejected["greenland_antarctica_duplicate"] = False
all_cmip6_compound_names = dups["CMIP6 Compound Name"].tolist()
for v in all_cmip6_compound_names:
    if (v.replace("Ant", "Gre") not in all_cmip6_compound_names) and (
        v.replace("Gre", "Ant") not in all_cmip6_compound_names
    ):
        print(f"Dupe but not from Antartica Greenland clash: {v}")
        continue

    raw_dr_not_rejected.loc[
        raw_dr_not_rejected["CMIP6 Compound Name"] == v,
        "greenland_antarctica_duplicate",
    ] = True

# %% [markdown]
# Answer 3: All of them. That's good, we don't have to deal with that headache.
# Having duplicated branded variables is fine and expected.
# Branded variables just define the variable.
# The data request defines the grid on which the variables should be reported.
# (I guess I disagree with Karl on this one,
# it makes sense to me that the data request would have 'duplicate' entries
# where the region is the only thing differing if they want to request a variable
# for greenland instead of antartica.)
#
# Conclusion: no issue, carry on.

# %% [markdown]
# Question 4: Are there duplicate CMIP7 compound names?

# %%
raw_dr_not_rejected[
    raw_dr_not_rejected["CMIP7 Compound Name"].duplicated(keep=False)
].sort_values("CMIP7 Compound Name")

# %% [markdown]
# Answer 4: Yes.
#
# Conclusion: bit messier. From my quick scan,
# these are just things to clean up but don't change content.
#
# - a lot of these seem to be duplicates that have just ended up
#   in different opportunities
#   or with different CMIP6 tables (hence different rows)
#   for whatever reason.
#   If that is correct, I'd suggest removing the duplicates.
#   If that is wrong, ignore me (although might be a good idea to write down what the difference is more clearly?)
# - some the CMIP7 compound name just seems misleading and can be ignored
#     -  e.g. the duplicate values for ocnBgchem.chl.tavg-u-hxy-sea.day.GLB
#        are just because this compound name has been created with an old branding algorithm
#        that doesn't realise that the branded names are actually
#        "chl_tavg-op20bar-hxy-sea" and "chlos_tavg-d0m-hxy-sea"
#        i.e. they're actually different quantities on different vertical levels
#     - same for siconc vs. siconca
# -

# %% [markdown]
# Ran out of time, next questions I would ask:
#
# - go through Karl's review and try to find the common themes to group issues more clearly/easily using code
