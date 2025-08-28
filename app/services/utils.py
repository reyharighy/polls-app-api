"""Module to provide some utilities to the application."""

import os
import re
from uuid import UUID
from typing import List
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
    poll_json = redis_client.get(name=f"poll:{poll_id}")

    if not indexing and not poll_json:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Poll of id {poll_id} is not found"}
        )

    return Poll.model_validate_json(poll_json) # type: ignore

def validate_poll_active(poll: Poll):
    """Validate if the poll is still active"""
    if not poll.is_active():
        raise HTTPException(
            status_code=410,
            detail={"msg": f"Poll of id {poll.id} has expired"}
        )

def validate_voter(poll_id: UUID, email: str):
    """Validate if the current voter makes the first vote"""
    if redis_client.sismember(f"poll:{poll_id}:emails", email):
        raise HTTPException(
            status_code=409,
            detail={"msg": f"Voter of email {email} has already voted in poll of id {poll_id}"}
        )

def get_option_description(poll: Poll, option_id: UUID) -> str:
    """Get the option description given the specified poll and option_id"""
    options = {option.id:option.description for option in poll.options}
    option_description = options.get(option_id)

    if not option_description:
        raise HTTPException(
            status_code=404,
            detail={"msg":f"Option of id {option_id} is not found in poll of id {poll.id}"}
        )

    return option_description

def get_all_polls() -> List[Poll]:
    """Method to retrieve all polls data from redis"""
    all_polls = []
    poll_only_pattern = re.compile(r"^poll:[A-Fa-f0-9-]+$")

    while True:
        cursor, keys = redis_client.scan(match="poll:*") # type: ignore

        filtered_keys: List[UUID] = [
            str(key).removeprefix("poll:")
            for key in keys if poll_only_pattern.match(key)
        ] # type: ignore

        for key in filtered_keys:
            poll = get_poll(
                poll_id=key,
                indexing=True
            )

            all_polls.append(poll)

        if cursor == 0:
            break

    return all_polls

def save_vote(vote: Vote):
    """Method to save vote data into redis"""
    vote_json = vote.model_dump_json()
    redis_client.set(f"vote:{vote.id}", vote_json)
    redis_client.sadd(f"poll:{vote.poll.id}:vote_ids", str(vote.id))
    redis_client.sadd(f"poll:{vote.poll.id}:emails", vote.voter.email)

def get_vote(poll_id: UUID, vote_id: UUID, indexing: bool = False) -> Vote:
    """Method to retrieve vote data from redis given the specified vote_id"""
    vote_json = redis_client.get(f"vote:{vote_id}")

    if not indexing and not vote_json:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Vote of id {vote_id} is not found"}
        )

    if not indexing and not redis_client.sismember(f"poll:{poll_id}:vote_ids", str(vote_id)):
        raise HTTPException(
            status_code=409,
            detail={"msg": f"Vote of id {vote_id} does not belong to poll of id {poll_id}"}
        )

    return Vote.model_validate_json(vote_json) # type: ignore

def get_all_votes(poll_id: UUID) -> List[Vote]:
    """Method to retrieve all votes data from redis"""
    all_votes = []

    vote_ids: List[UUID] = redis_client.smembers(f"poll:{poll_id}:vote_ids") # type: ignore

    for vote_id in vote_ids:
        vote: Vote = get_vote(
            poll_id=poll_id,
            vote_id=vote_id,
            indexing=True
        )

        all_votes.append(vote)

    return all_votes
