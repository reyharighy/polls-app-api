"""Entry point to start a web server of a polling application using FastAPI."""

from fastapi import FastAPI
from app.api import polls, votes, results
from app.config import APPLICATION_METADATA

app = FastAPI(
    title=APPLICATION_METADATA["title"],
    description=APPLICATION_METADATA["description"],
    version=APPLICATION_METADATA["version"],
    openapi_tags=APPLICATION_METADATA["openapi_tags"],
    contact=APPLICATION_METADATA["contact"]
)

app.include_router(polls.router, prefix="/polls", tags=["polls"])
app.include_router(votes.router, prefix="/polls/{poll_id}/votes", tags=["votes"])
app.include_router(results.router, prefix="/polls/{poll_id}/results", tags=["results"])
