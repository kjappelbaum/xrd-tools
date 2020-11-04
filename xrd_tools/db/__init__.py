# -*- coding: utf-8 -*-
"""Utilities of handling the database"""
from motor.motor_asyncio import AsyncIOMotorClient

# Motor presents a coroutine-based API for non-blocking access
# to MongoDB from Tornado or asyncio.
from ..config import MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT, MONGODB_URL


class DataBase:  # pylint:disable=missing-class-docstring, too-few-public-methods
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    """Return a client"""
    return db.client


async def connect_to_mongo():
    """Connect to the mongo db for the app"""
    db.client = AsyncIOMotorClient(
        str(MONGODB_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT,
    )


async def close_mongo_connection():
    """Close the connection"""
    db.client.close()
