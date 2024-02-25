from fastapi.concurrency import asynccontextmanager
from .app import FastAPI
__all__ = []

async def startup():
    ...

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield 
    await shutdown()
