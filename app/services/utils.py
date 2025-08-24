"""Module to provide some utilities to the application."""

import os
from uuid import UUID
from typing import Optional
from redis import Redis
from app.models.poll import Poll

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT) # type: ignore

def save_poll(poll: Poll):
    """Method to save poll data into redis"""
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)

def get_poll(poll_id: UUID) -> Optional[Poll]:
    """Method to retrieve poll data from redis based-on poll_id"""
    poll_json = redis_client.get(f"poll:{poll_id}")

    if poll_json:
        return Poll.model_validate_json(poll_json) # type: ignore

    return None
