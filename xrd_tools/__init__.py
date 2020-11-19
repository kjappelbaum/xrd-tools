# -*- coding: utf-8 -*-
# pylint:disable=cyclic-import
"""
REST-API serving XRD prediction tools
"""

__version__: str = "0.0.5"

# Add imports here
from .xrd_app import app  # pylint:disable=wrong-import-position
