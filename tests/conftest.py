from typing import Any
from typing import Generator

import certifi
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from farmtool.cows_api import router


def start_application():
    app = FastAPI()
    app.mongodb_client = AsyncIOMotorClient("mongodb+srv://Bishara:MongoDBBishara@cluster0.x8huj.mongodb.net"
                                            "/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
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
