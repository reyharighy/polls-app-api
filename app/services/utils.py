"""Module to provide some utilities to the application."""

import os
from uuid import UUID
from redis import Redis
from fastapi import HTTPException
from app.models.poll import Poll
from app.models.vote import Vote

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT) # type: ignore

def save_poll(poll: Poll):
    """Method to save poll data into redis"""
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)

def get_poll(poll_id: UUID) -> Poll:
    """Method to retrieve poll data from redis based-on poll_id"""
    poll_json = redis_client.get(f"poll:{poll_id}")

    if not poll_json:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Poll of id {poll_id} is not found"}
        )

    return Poll.model_validate_json(poll_json) # type: ignore

def check_poll_is_active(poll: Poll):
    """Check if the poll is still active given specified option_id"""
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

def save_vote(vote: Vote):
    """Method to save vote data into redis"""
    vote_json = vote.model_dump_json()
    redis_client.set(f"vote:{vote.id}", vote_json)
