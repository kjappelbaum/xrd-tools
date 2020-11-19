# -*- coding: utf-8 -*-
# pylint:disable=cyclic-import
"""
REST-API serving XRD prediction tools
"""
import os
import logging
from fastapi.logger import logger
from diskcache import Cache

__version__: str = "0.0.5"


LOGLEVEL = os.getenv("LOGLEVEL")

if LOGLEVEL == "debug":
    logger.setLevel(logging.DEBUG)


pattern_cache = Cache(size_limit=2 * 10 ** 7, disk_min_file_size=0)
laue_cache = Cache(size_limit=2 * 10 ** 7, disk_min_file_size=0)

# Add imports here
from .xrd_app import app  # pylint:disable=wrong-import-position
