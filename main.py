"""Entry point to start a web server of a FastAPI application."""

from uuid import UUID
from fastapi import FastAPI, HTTPException
from app.models.poll import PollCreate
from app.services.utils import save_poll, get_poll

app = FastAPI()

@app.post("/polls/create")
def create_poll(poll: PollCreate):
    """Endpoint to create a new poll."""
    new_poll = poll.create()
    save_poll(poll=new_poll)

    return {
        "msg": "Poll created successfully",
        "poll": new_poll
    }

@app.get("/polls/{poll_id}")
def show_poll(poll_id: UUID):
    """Endpoint to retrieve a poll."""
    poll = get_poll(poll_id=poll_id)

    if not poll:
        raise HTTPException(
            status_code=404,
            detail=f"Poll with id {poll_id} is not found"
        )

    return poll
