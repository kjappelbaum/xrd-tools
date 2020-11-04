# -*- coding: utf-8 -*-
# pylint:disable=cyclic-import
"""
REST-API serving XRD prediction tools
"""

# Handle versioneer
from ._version import get_versions

versions = get_versions()
__version__: str = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions

# Add imports here
from .xrd_app import app  # pylint:disable=wrong-import-position
