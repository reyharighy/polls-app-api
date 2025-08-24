"""Entry point to start a web server of a FastAPI application."""

from fastapi import FastAPI
from app.api import polls

app = FastAPI()

app.include_router(polls.router, prefix="/polls", tags=["polls"])
