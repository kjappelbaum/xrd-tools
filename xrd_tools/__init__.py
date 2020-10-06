# -*- coding: utf-8 -*-
"""Calculation happens here"""
import pymatgen
import pytojcamp
from func_timeout import func_set_timeout
from pymatgen import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pytojcamp import from_dict


@func_set_timeout(40)
def calculate_pattern(structure, wavelength, return_jcamp):
    """Use pymatgen to calculate a PXRD pattern based on a pymatgen structure"""
    calculator = XRDCalculator(wavelength=wavelength)
    pattern = calculator.get_pattern(structure)
    two_theta = list(pattern.x)
    intensity = list(pattern.y)
    hkls = pattern.hkls

    output_dict = {
        "x": two_theta,
        "y": intensity,
        "hkls": hkls,
    }

    if return_jcamp:

        jcamp = from_dict(
            {
                "x": {
                    "data": output_dict["x"],
                    "unit": "°",
                    "type": "INDEPENDENT",
                    "name": "2 theta",
                },
                "y": {
                    "data": output_dict["y"],
                    "type": "DEPENDENT",
                    "unit": "",
                    "name": "intensity",
                },
            },
            data_type="Predicted PXRD pattern",
            origin=f"Pymatgen version {pymatgen.__version__}\
                        converted to JCAMP with pytojcamp version\
                             {pytojcamp.__version__}",
            meta={"wavelength": wavelength},
        )

        output_dict["jcamp"] = jcamp

    return output_dict
