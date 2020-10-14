# -*- coding: utf-8 -*-
"""
REST-API serving XRD prediction tools
"""
import logging

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from fastapi.responses import HTMLResponse

from . import __version__
from .core import calculate_pattern, calculate_laue_pattern
from .models import XRDInput, XRDResponse, LatticeInput

app = FastAPI(
    title="XRD prediction",
    description="Offers XRD prediction tools",
    version=__version__,
)

logger = logging.getLogger("api")


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>XRD prediction</title>
        </head>
        <h1> XRD prediction </h1>
        <body>
            <p>This webservice provides XRD prediction tools.</p>
            <p>Find the docs at <a href="./docs">/docs</a> and the openAPI specfication at <a href="./openapi.json">/openapi.json</a>.</p>
        </body>
    </html>
    """


@app.get("/version")
def read_version():
    return {"version": __version__}


@app.post("/predictxrd", response_model=XRDResponse)
def predict_xrd(parameters: XRDInput):
    try:
        return calculate_pattern(
            parameters.fileContent,
            parameters.extension,
            parameters.wavelength,
            parameters.jcamp,
        )
    except Exception as excep:
        logger.error("XRD prediction failed {}".format(excep))
        raise HTTPException(status_code=400, detail="XRD prediction failed")


@app.post("/latticepattern", response_model=XRDResponse)
def predict_laue(parameters: LatticeInput):
    try:

        return calculate_laue_pattern(
            parameters.a,
            parameters.b,
            parameters.c,
            parameters.alpha,
            parameters.beta,
            parameters.gamma,
            parameters.wavelength,
            parameters.jcamp,
        )
    except Exception as excep:
        logger.error("XRD prediction failed {}".format(excep))
        raise HTTPException(status_code=400, detail="XRD prediction failed")
