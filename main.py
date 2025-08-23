"""Entry point to start a web server of a FastAPI application."""

from fastapi import FastAPI
from app.models.poll import PollCreate

app = FastAPI()

@app.post("/polls/create")
def create_poll(poll: PollCreate):
    """Entrypoint to create a new poll."""
    print(poll)
    new_poll = poll.create()

    return {
        "msg": "Poll created successfully",
        "poll": new_poll
    }
