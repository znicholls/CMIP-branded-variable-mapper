time_labels_dimensions = {
    "time": "tavg",
    "time1": "tpt",
    "time2": "tclm",
    "time3": "tcld"
}


time_labels_cell_methods = {
    "time: max": "tstat",
    "time: min": "tstat",
    "time: sum": "tsum",
}

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
    "depth100m": "z0100",
    "olayer100m": "d100m",
    "olayer100m": "z0100",
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

area_labels = {
    "where air": "air",
    "where cloud": "cl",
    "where convective_cloud": "ccl",
    "where crops": "crp",
    "where floating_ice_shelf": "fis",
    "where grounded_ice_sheet": "gis",
    "where ice_free_sea": "ifs",
    "where ice_sheet": "is",
    "where land": "lnd",
    "where land_ice": "li",
    "where natural_grasses": "ng",
    "where pastures": "pst",
    "where sea": "sea",
    "where sea_ice": "si",
    "where sea_ice_melt_pond": "simp",
    "where sea_ice_ridges": "sir",
    "where sector": "lus",
    "where shrubs": "shb",
    "where snow": "sn",
    "where stratiform_cloud": "scl",
    "where trees": "tree",
    "where unfrozen_soil": "ufs",
    "where vegetation": "veg",
    "where wetland": "wl"
}


def _get_label(label_options: dict, label_in: str, default: str) -> str:
    
    out_label = default
    
    for label,translation in label_options.items():
            if label in label_in:
                out_label = f"{translation}"
    
    return out_label



def cmip_branded_variable_mapper(variable_name: str, cell_methods: str, dimensions:str) -> str:
    
    """
    Constructs a CMIP7 branded variable name based on variable metadata from CMIP6.
    
    Args:
        variable_name: Name of the variable in CMIP6 and CMIP7
        cell_methods: Cell methods string containing processing information
        dimensions: Dimensions string containing variable dimensions
        
    Returns: CMIP7 branded variable name 
        
    """

    # rename nan entries to empty string
    if cell_methods != cell_methods:
        cell_methods = ""

    if "time: max" not in cell_methods and "time: min" not in cell_methods and "time: sum" not in cell_methods: 
        
        temporalLabelDD = _get_label(time_labels_dimensions, dimensions, 'ti')
        
    else: 
        
        temporalLabelDD = _get_label(time_labels_cell_methods, cell_methods, 'ti')
        
    verticalLabelDD = _get_label(vertical_labels, dimensions, 'u')

    horizontalLabelDD = _get_label(horizontal_labels, dimensions, 'hm')

    areaLabelDD = _get_label(area_labels, cell_methods, 'u')
            
    return f"{variable_name}_{temporalLabelDD}-{verticalLabelDD}-{horizontalLabelDD}-{areaLabelDD}"

