from typing import Any
from typing import Generator

import certifi
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from farmtool.cows_api import router
from dotenv import load_dotenv
import os
import logging


# load environment variables from .env
load_dotenv(".env")

logging.basicConfig(filename='test_app.log', format='%(asctime)s - farmtool - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def start_application():
    app = FastAPI()
    app.logger = logging.getLogger()
    app.mongodb_client = AsyncIOMotorClient(os.environ.get("MONGODB_CONNECTION_STRING"), tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client["test_cowshed"]

    app.include_router(router)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    _app = start_application()
    yield _app


@pytest.fixture(scope="function")
def client(
        app: FastAPI
) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client
