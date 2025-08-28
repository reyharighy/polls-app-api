"""Module to define all HTTP endpoints related to the poll model."""

from uuid import UUID
from fastapi import APIRouter
from app.models.poll import PollCreate
from app.services.utils import save_poll, get_poll, get_all_polls, delete_poll

router = APIRouter()

@router.post("/create")
def create_poll(poll: PollCreate):
    """Endpoint to create a new poll."""
    new_poll = poll.create()
    save_poll(poll=new_poll)

    return {
        "msg": "Poll created successfully",
        "poll": new_poll
    }

@router.get("/{poll_id}")
def show_poll(poll_id: UUID):
    """Endpoint to retrieve a poll."""
    return get_poll(poll_id=poll_id)

@router.get("")
def index_poll():
    """Endpoint to retrieve all polls."""
    return get_all_polls()

@router.delete("/{poll_id}")
def destroy_poll(poll_id: UUID):
    """Endpoint to delete a poll."""
    poll = get_poll(poll_id=poll_id)

    delete_poll(poll_id=poll.id)

    return {
        "msg": "Poll deleted successfully",
        "poll": poll
    }
