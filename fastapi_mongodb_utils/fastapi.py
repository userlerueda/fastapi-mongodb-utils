# -*- coding: utf-8 -*-
__author__ = "Luis Rueda, Jairo Leon"
__email__ = "userlerueda@gmail.com, jlr060@gmail.com"

import typing

from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database


class CustomFastAPI(FastAPI):
    """Custom FastAPI class."""

    # Async Client and Database
    mongodb_aclient: AsyncIOMotorClient
    adb: AsyncIOMotorDatabase

    # Sync Client and Database
    mongodb_client: MongoClient
    db: Database


if typing.TYPE_CHECKING:  # pragma: no cover

    class FastAPIRequest(Request):
        """Custom FastAPI Request class."""

        app: CustomFastAPI

else:
    FastAPIRequest = Request
