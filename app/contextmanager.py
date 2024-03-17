from fastapi.concurrency import asynccontextmanager
from schemas.dynamic import DynamicModels
from fastapi import FastAPI

async def startup():
    await DynamicModels.generate()

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield 
    await shutdown()
