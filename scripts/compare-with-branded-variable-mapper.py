"""
Compare outputs from our software with those from the data request software
"""

import json
import urllib.request

from cmip_branded_variable_mapper import map_to_cmip_branded_variable

# See note in dr_compute_brand for why this doesn't use the DR API
from cmip_branded_variable_mapper.dr_compute_brand import (
    compute_brand as compute_brand_dr,
)


def main() -> None:
    """Run the comparison"""
    VARIABLE_URL = "https://raw.githubusercontent.com/CMIP-Data-Request/CMIP7_DReq_Software/a466f0d4dddef9a3234134b1fc463f901135f37b/scripts/examples/variables_v1.2.1.json"
    with urllib.request.urlopen(VARIABLE_URL) as url:
        variables = json.load(url)

    differences = 0
    for cn, info in variables["Compound Name"].items():
        variable_name = info["physical_parameter_name"]
        cell_methods = info["cell_methods"]
        dimensions = info["dimensions"].split(" ")

        branded_variable_dr = compute_brand_dr(
            # Only used for region,
            # hence we don't care about the value for this comparison.
            var_name="junk",
            param_name=variable_name,
            freq_name=info["frequency"],
            cell_methods=cell_methods,
            dimensions=dimensions,
        )
        branded_variable_dr_components = branded_variable_dr.split("-")
        branded_variable_dr_corrected = "_".join(
            [
                branded_variable_dr_components[0],
                "-".join(branded_variable_dr_components[1:]),
            ]
        )

        branded_variable_here = map_to_cmip_branded_variable(
            variable_name=variable_name,
            cell_methods=cell_methods,
            dimensions=dimensions,
        )
        if branded_variable_dr_corrected != branded_variable_here:
            print(cn)
            print(json.dumps(info, sort_keys=True))
            print(f"{branded_variable_dr_corrected=}")
            print(f"{branded_variable_here=}")
            print()
            differences += 1

    print(f"{differences=}")


if __name__ == "__main__":
    main()
