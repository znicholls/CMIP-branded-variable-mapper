"""
Mapping from CMIP variable and other information to branded variable names.
"""

import importlib.metadata

from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable

__version__ = importlib.metadata.version("cmip_branded_variable_mapper")

__all__ = ["map_to_cmip_branded_variable"]
