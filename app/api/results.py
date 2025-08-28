"""Module to define all HTTP endpoints related to the result model."""

from uuid import UUID
from fastapi import APIRouter
from app.models.result import Result, ResultPoll
from app.services.utils import get_poll, vote_results

router = APIRouter()

@router.get("")
def show_result(poll_id: UUID):
    """Get the result of voting given the specified poll_id."""
    poll = get_poll(poll_id=poll_id)
    total_votes, votes = vote_results(poll=poll)

    return Result(
        poll=ResultPoll(
            id=poll.id,
            title=poll.title,
            expires_at=poll.expires_at,
            created_at=poll.created_at
        ),
        total_votes=total_votes,
        votes=votes
    )
