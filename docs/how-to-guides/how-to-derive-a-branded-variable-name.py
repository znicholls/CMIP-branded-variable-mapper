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

# %% [markdown] editable=true slideshow={"slide_type": ""}
# # How to derive a branded variable name
#
# Here we show how to translate "old" CMIP variable names
# plus information about dimensions
# and [cell methods](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html#cell-methods).
# into CMIP branded variables.

# %% [markdown]
# ## Imports

# %%
from cmip_branded_variable_mapper import map_to_cmip_branded_variable

# %% [markdown]
# ## Creating branded variables
#
# The basic API is very simple:
# [map_to_cmip_branded_variable](../../api/cmip_branded_variable_mapper/#cmip_branded_variable_mapper.map_to_cmip_branded_variable)
# In the simplest case, all we need is the old variable name
# and the dimensions (as a tuple, not a whitespace-separated string).

# %%
ugrido_branded_variable = map_to_cmip_branded_variable(
    variable_name="ugrido", cell_methods=None, dimensions=("longitude", "latitude")
)
ugrido_branded_variable

# %% [markdown]
# This use case is rare.
# In most cases, you also need the cell methods.

# %%
tas_branded_variable = map_to_cmip_branded_variable(
    variable_name="tas",
    cell_methods="area: time: mean",
    dimensions=("longitude", "latitude", "time", "height2m"),
)
tas_branded_variable

# %%
tos_branded_variable = map_to_cmip_branded_variable(
    variable_name="tos",
    cell_methods="area: mean where sea time: point",
    dimensions=("longitude", "latitude", "time1"),
)
tos_branded_variable

# %%
hfds_branded_variable = map_to_cmip_branded_variable(
    variable_name="hfds",
    cell_methods="area: mean where sea time: mean",
    dimensions=("longitude", "latitude", "time"),
)
hfds_branded_variable

# %% [markdown]
# ## Notes
#
# There are clearly many things missing here.
# For example, the package provides no information
# about what combinations of variable names,
# cell methods and dimensions are valid.
# These are good questions,
# but they're also outside the remit of this package.
# If you do have insights/thoughts,
# please [raise an issue](https://github.com/znicholls/CMIP-branded-variable-mapper/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen)
# and we will do our best to put this information in a more useful place.
