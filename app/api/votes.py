"""Module to define all HTTP endpoints related to the vote model."""

from uuid import UUID
from fastapi import APIRouter
from app.models.vote import VoteCreate
from app.services.utils import save_vote, get_poll, get_option_description

router = APIRouter()

@router.post('/{poll_id}/create')
def create_vote(poll_id: UUID, vote: VoteCreate):
    """Endpoint to create a new vote upon a poll."""
    poll = get_poll(poll_id=poll_id)

    option_description = get_option_description(
        poll=poll,
        option_id=vote.option_id
    )

    new_vote = vote.create(
        poll=poll,
        option_description=option_description
    )

    save_vote(new_vote)

    return {
        "msg": "Vote created successfully",
        "vote": new_vote
    }
