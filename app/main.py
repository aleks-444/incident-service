from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router
from app.migrations import run_migrations


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    await run_migrations()

    yield


app = FastAPI(
    title="Incident API",
    description="API для учёта инцидентов",
    lifespan=lifespan
)

app.include_router(router, prefix="/incidents", tags=["incidents"])


@app.get("/")
async def read_root():
    return {"message": "Incident API is running"}