from typing import Dict

from fastapi import FastAPI

from app.routers import leads, users
from app.services.database import create_database

app = FastAPI(title="Lead Management API")


@app.on_event("startup")
async def startup_event() -> None:
    create_database()


@app.get("/", summary="Status")
async def root() -> Dict[str, str]:
    return {"message": "The server is running"}


app.include_router(users.router)
app.include_router(leads.router)
