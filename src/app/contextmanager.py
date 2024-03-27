from fastapi.concurrency import asynccontextmanager
from services.dynamic import CamerusService
from fastapi import FastAPI
from units_of_work.camerus import CamerusUOW

async def startup():
    await CamerusService(CamerusUOW()).generate()

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield 
    await shutdown()
