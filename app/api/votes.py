"""Module to define all HTTP endpoints related to the vote model."""

from uuid import UUID
from fastapi import APIRouter
from app.models.vote import VoteCreate
from app.services.utils import (
    get_poll, get_option_description, 
    save_vote, get_vote, get_all_votes, 
    validate_voter
)

router = APIRouter()

@router.post("/create")
def create_vote(poll_id: UUID, vote: VoteCreate):
    """Endpoint to create a new vote upon a poll."""
    validate_voter(
        poll_id=poll_id,
        email=vote.voter.email
    )

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

@router.get("/{vote_id}")
def show_vote(poll_id: UUID, vote_id: UUID):
    """Endpoint to retrieve a vote."""
    return get_vote(
        poll_id=poll_id,
        vote_id=vote_id
    )

@router.get("")
def index_vote(poll_id: UUID):
    """Endpoint to retrieve all votes."""
    return get_all_votes(poll_id=poll_id)
