# -*- coding: utf-8 -*-
"""
REST-API serving XRD prediction tools
"""

# Handle versioneer
from ._version import get_versions

# Add imports here
from .xrd_tools import app

versions = get_versions()
__version__: str = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
