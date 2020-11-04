# -*- coding: utf-8 -*-
"""Retrieve a pattern from the database"""
from .. import __version__
from ..config import DBNAME, PATTERN_COLLECITON_NAME
from . import AsyncIOMotorClient


def pattern_db_helper(pattern) -> dict:
    """Convert an entry from the Mongo DB to
    response following the DataBaseEntry model"""
    return {
        "id": str(pattern["_id"]),
        "x": pattern["pattern"]["x"],
        "y": pattern["pattern"]["y"],
        "hkls": pattern["pattern"]["hkls"],
        "link": pattern["link"],
        "dbName": pattern["id"],
        "cif": pattern["cif"],
        "apiVersion": __version__,
    }


async def get_pattern(conn: AsyncIOMotorClient, db_name: str):
    """Find a database row based on the database identifier
    like the COD number or the CSD reference code"""
    row = await conn[DBNAME][PATTERN_COLLECITON_NAME].find_one({"id": db_name})
    if row:
        return pattern_db_helper(row)
