from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Incident API",
    description="API для учёта инцидентов",
    lifespan=lifespan
)

app.include_router(router, prefix="/incidents", tags=["incidents"])

@app.get("/")
def read_root():
    return {"message": "Incident API is running"}