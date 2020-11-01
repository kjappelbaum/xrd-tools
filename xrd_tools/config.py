# -*- coding: utf-8 -*-
"""Settings for the app"""
import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", "5"))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", "5"))

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
    MONGO_DB = os.getenv("MONGO_DB", "fastapi")

    MONGODB_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"


DBNAME = "xrd-patterns"
PATTERN_COLLECITON_NAME = "patterns"
