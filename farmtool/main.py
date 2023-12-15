import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .cows_api import router as CowsApiRouter
import certifi
import logging
from dotenv import load_dotenv
import os

# load environment variables from .env
load_dotenv(".env")

logging.basicConfig(filename='app.log', format='%(asctime)s - farmtool - %(levelname)s - %(message)s',
                    level=logging.INFO)

# initiate fastAPI 
app = FastAPI(
    title="farmtool",
    description="Automate and Handle Cowshed",
    version="1.0.0",
)


@app.on_event("startup")
async def on_start():
    """initiate logger and db_client"""
    app.logger = logging.getLogger()
    os.environ.get("MONGODB_CONNECTION_STRING")
    app.mongodb_client = AsyncIOMotorClient(os.environ["MONGODB_CONNECTION_STRING"], tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client["CowShed"]


@app.on_event("shutdown")
async def on_shutdown():
    """close db_client session"""
    app.mongodb_client.close()

app.include_router(CowsApiRouter)

@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")

