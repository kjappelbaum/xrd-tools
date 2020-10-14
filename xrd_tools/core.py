# -*- coding: utf-8 -*-
"""Calculation happens here"""
import pymatgen
import pytojcamp
from func_timeout import func_set_timeout
from .laue_predictor import LatticeXRDCalculator
from pymatgen import Structure, Lattice
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pytojcamp import from_dict
from . import __version__


@func_set_timeout(40)
def calculate_pattern(
    filecontent, extension="cif", wavelength="CuKa", return_jcamp=False
):
    """Use pymatgen to calculate a PXRD pattern based on a pymatgen structure"""
    structure = Structure.from_str(filecontent, fmt=extension)
    calculator = XRDCalculator(wavelength=wavelength)
    pattern = calculator.get_pattern(structure)
    two_theta = list(pattern.x)
    intensity = list(pattern.y)
    hkls = pattern.hkls

    output_dict = {
        "x": two_theta,
        "y": intensity,
        "hkls": hkls,
        "api_version": __version__,
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


@func_set_timeout(40)
def calculate_laue_pattern(
    a, b, c, alpha, beta, gamma, wavelength="CuKa", return_jcamp=False
):
    lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma)
    structure = Structure(lattice=lattice, species=[], coords=[])
    calculator = LatticeXRDCalculator(wavelength=wavelength)
    pattern = calculator.get_pattern(structure)

    output_dict = {
        "x": list(pattern.x),
        "y": list(pattern.y),
        "hkls": pattern.hkls,
        "api_version": __version__,
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
