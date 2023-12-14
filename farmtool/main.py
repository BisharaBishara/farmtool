import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .cows_api import router as CowsApiRouter
import certifi
import logging
from dotenv import load_dotenv
import os

print(load_dotenv(".env"))

logging.basicConfig(filename='app.log', format='%(asctime)s - farmtool - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
app = FastAPI(
    title="farmtools",
    description="Automate and Handle Cowshed",
    version="1.0.0",
)


@app.on_event("startup")
async def start_db_client():
    
    app.logger = logging.getLogger()
    os.environ.get("MONGODB_CONNECTION_STRING")
    app.mongodb_client = AsyncIOMotorClient(os.environ["MONGODB_CONNECTION_STRING"], tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client["CowShed"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(CowsApiRouter)

@app.get("/")
async def redirect():
    return RedirectResponse(url="/docs")

