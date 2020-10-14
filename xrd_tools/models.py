# -*- coding: utf-8 -*-
from . import __version__
from typing import Optional
from pymatgen.analysis.diffraction.xrd import WAVELENGTHS
from pydantic import BaseModel, validator

EXTENSIONS = "cif"


class XRDResponse(BaseModel):
    x: list
    y: list
    hkls: list
    jcamp: Optional[str]
    api_version: Optional[str] = __version__


class XRDInput(BaseModel):
    fileContent: str
    wavelength: Optional[str] = "CuKa"
    extension: Optional[str] = "cif"
    jcamp: Optional[bool] = False

    @validator("wavelength")
    def wavelength_must_be_known(cls, v):
        if v not in list(WAVELENGTHS.keys()):
            raise ValueError(
                "Wavelength must be in {}".format(", ".join(list(WAVELENGTHS.keys())))
            )
        return v

    @validator("extension")
    def extension_must_be_known(cls, v):
        if v not in EXTENSIONS:
            raise ValueError("Extension must be in {}".format(", ".join(EXTENSIONS)))
        return v


class LatticeInput(BaseModel):
    a: float
    b: float
    c: float
    alpha: float
    beta: float
    gamma: float
    wavelength: Optional[str] = "CuKa"
    jcamp: Optional[bool] = False

    @validator("wavelength")
    def wavelength_must_be_known(cls, v):
        if v not in list(WAVELENGTHS.keys()):
            raise ValueError(
                "Wavelength must be in {}".format(", ".join(list(WAVELENGTHS.keys())))
            )
        return v
