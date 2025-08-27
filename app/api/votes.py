"""Module to define all HTTP endpoints related to the vote model."""

from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.models.vote import VoteCreate
from app.services.utils import save_vote, get_poll

router = APIRouter()

@router.post('/{poll_id}/create')
def create_vote(poll_id: UUID, vote: VoteCreate):
    """Endpoint to create a new vote upon a poll."""
    poll = get_poll(poll_id=poll_id)
    options = {choice.id:choice.description for choice in poll.options}
    option_description = options.get(vote.option_id)

    if not option_description:
        raise HTTPException(
            status_code=404,
            detail={"msg":f"Option of id {vote.option_id} is not found in poll of id {poll.id}"}
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
