"""Module to provide some utilities to the application."""

import os
from uuid import UUID
from redis import Redis
from fastapi import HTTPException
from app.models.poll import Poll
from app.models.vote import Vote

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis_client = Redis(
    host=REDIS_HOST, # type: ignore
    port=REDIS_PORT, # type: ignore
    decode_responses=True
)

def save_poll(poll: Poll):
    """Method to save poll data into redis"""
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)

def get_poll(poll_id: UUID, indexing: bool = False) -> Poll:
    """Method to retrieve poll data from redis given the specified poll_id"""
    poll_json = redis_client.get(f"poll:{poll_id}")

    if not poll_json and not indexing:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Poll of id {poll_id} is not found"}
        )

    return Poll.model_validate_json(poll_json) # type: ignore

def check_poll_is_active(poll: Poll):
    """Check if the poll is still active given the specified poll_id from path parameter"""
    if not poll.is_active():
        raise HTTPException(
            status_code=410,
            detail={"msg": f"Poll of id {poll.id} has expired"}
        )

def get_option_description(poll: Poll, option_id: UUID) -> str:
    """
    Get the option description with the following requirements:
    1. Check if the given poll is still active.
    2. Check if the option_id is valid given the specified poll.
    3. If option is valid, return the option description.
    """

    check_poll_is_active(poll=poll)
    options = {choice.id:choice.description for choice in poll.options}
    option_description = options.get(option_id)

    if not option_description:
        raise HTTPException(
            status_code=404,
            detail={"msg":f"Option of id {option_id} is not found in poll of id {poll.id}"}
        )

    return option_description

def get_all_polls():
    """Method to retrieve all polls data from redis"""
    all_polls = []

    _, keys = redis_client.scan(match="poll:*") # type: ignore

    for key in keys:
        poll = get_poll(
            poll_id=key.replace("poll:", ""),
            indexing=True
        )

        all_polls.append(poll)

    return all_polls

def save_vote(vote: Vote):
    """Method to save vote data into redis"""
    vote_json = vote.model_dump_json()
    redis_client.set(f"vote:{vote.id}", vote_json)

def get_vote(poll_id: UUID, vote_id: UUID, indexing: bool = False) -> Vote:
    """Method to retrieve vote data from redis given the specified vote_id"""
    vote_json = redis_client.get(f"vote:{vote_id}")

    if not vote_json and not indexing:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Vote of id {vote_id} is not found"}
        )

    vote = Vote.model_validate_json(vote_json) # type: ignore

    if vote.poll.id != poll_id and not indexing:
        raise HTTPException(
            status_code=409,
            detail={"msg": f"Vote of id {vote_id} does not belong to poll of id {poll_id}"}
        )

    return vote

def get_all_votes(poll_id: UUID):
    """Method to retrieve all votes data from redis"""
    all_votes = []

    _, keys = redis_client.scan(match="vote:*") # type: ignore

    for key in keys:
        vote: Vote = get_vote(
            poll_id=poll_id,
            vote_id=key.replace("vote:", ""),
            indexing=True
        )

        if vote.poll.id == poll_id:
            all_votes.append(vote)

    return all_votes

def validate_voter(poll_id: UUID, email: str):
    """Validate if the current voter makes the first vote"""
    votes: list[Vote] = get_all_votes(poll_id=poll_id)

    if email in [vote_.voter.email for vote_ in votes]:
        raise HTTPException(
            status_code=409,
            detail={"msg": f"Voter of email {email} has already voted in poll of id {poll_id}"}
        )
