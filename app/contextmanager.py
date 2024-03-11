from fastapi.concurrency import asynccontextmanager
from schemas.dynamic import DynamicModels


async def startup():
    await DynamicModels.generate()

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app):
    await startup()
    yield 
    await shutdown()
