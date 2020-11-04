# -*- coding: utf-8 -*-
# pylint:disable=logging-format-interpolation
"""
REST-API serving XRD prediction tools
"""
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from . import __version__
from .config import ALLOWED_HOSTS
from .core import calculate_laue_pattern, calculate_pattern
from .db import (
    AsyncIOMotorClient,
    close_mongo_connection,
    connect_to_mongo,
    get_database,
)
from .db.db_lookup import get_pattern
from .models import DataBaseEntry, LatticeInput, XRDInput, XRDResponse

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]


app = FastAPI(
    title="XRD prediction",
    description="Offers XRD prediction tools",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


logger = logging.getLogger("api")


@app.get("/", response_class=HTMLResponse)
def root():
    """Return some HTML on the landing page"""
    return """
    <html>
        <head>
            <title>XRD tools</title>
        </head>
        <h1> XRD tools </h1>
        <body>
            <p>This webservice provides XRD tools (prediction and database lookup).</p>
            <p>Find the docs at <a href="./docs">/docs</a> and the openAPI specfication at <a href="./openapi.json">/openapi.json</a>.</p>
        </body>
    </html>
    """


@app.get("/version")
def read_version():
    """Return version for health checks"""
    return {"version": __version__}


@app.post("/predictxrd", response_model=XRDResponse)
def predict_xrd(parameters: XRDInput):
    """Use pymatgen to predict an XRD pattern for
    a CIF"""
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
    """Use pymatgen to predict a XRD reflex positions
    for a cell"""
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


@app.get("/getpattern", response_model=DataBaseEntry)
async def retrieve_pattern(  # pylint:disable=invalid-name
    dbName: str, db: AsyncIOMotorClient = Depends(get_database)
):
    """Look up a XRD pattern and CIF in the COD and CoRE-MOF database
    based on the database identifier"""
    try:
        response = await get_pattern(db, dbName)
        return response
    except Exception as excep:
        logger.error("Pattern lookup failed {}".format(excep))
        raise HTTPException(status_code=400, detail="Pattern lookup failed")
