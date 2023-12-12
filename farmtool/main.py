import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from .cows_api import router as CowsApiRouter
import certifi

app = FastAPI(
    title="farmtools",
    description="Automate and Handle Cowshed",
    version="1.0.0",
)


@app.on_event("startup")
async def start_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb+srv://Bishara:MongoDBBishara@cluster0.x8huj.mongodb.net"
                                            "/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client["CowShed"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(CowsApiRouter)
