# -*- coding: utf-8 -*-
"""Calculation happens here"""
import pymatgen
import pytojcamp
from func_timeout import func_set_timeout
from pymatgen import Lattice, Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pytojcamp import from_dict

from . import __version__
from .laue_predictor import LatticeXRDCalculator


@func_set_timeout(60)
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
        "apiVersion": __version__,
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


@func_set_timeout(60)
def calculate_laue_pattern(  # pylint:disable=invalid-name,too-many-arguments
    a: float,
    b: float,
    c: float,
    alpha: float,
    beta: float,
    gamma: float,
    wavelength: str = "CuKa",
    return_jcamp: bool = False,
) -> dict:
    """Calculate the diffraction positions for a cell

    Args:
        a (float): Cell parameter a
        b (float): Cell parameter b
        c (float): Cell parameter c
        alpha (float): Cell angle alpha
        beta (float): Cell angle beta
        gamma (float): Cell angle gamma
        wavelength (str, optional): Wavelength that is used
            for the calculation of the reflex positions.
            According to the Bragg equation that influences the spacing
            of the reflexes
            Defaults to "CuKa".
        return_jcamp (bool, optional): If true, also returns a JCAMP as string.
            Defaults to False.

    Returns:
        dict: [description]
    """
    lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma)
    structure = Structure(lattice=lattice, species=[], coords=[])
    calculator = LatticeXRDCalculator(wavelength=wavelength)
    pattern = calculator.get_pattern(structure)

    output_dict = {
        "x": list(pattern.x),
        "y": list(pattern.y),
        "hkls": pattern.hkls,
        "apiVersion": __version__,
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
