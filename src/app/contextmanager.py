from fastapi.concurrency import asynccontextmanager
from repositories.camerus import CamerusRepo
from services.dynamic import CamerusService
from fastapi import FastAPI

async def startup():
    await CamerusService(CamerusRepo).generate()

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield 
    await shutdown()
