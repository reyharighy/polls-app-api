"""Module to define the result model."""

from uuid import UUID
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.option import Option

class ResultPoll(BaseModel):
    """Define the information of the poll when polling result is requested."""
    id: UUID
    title: str
    expires_at: Optional[datetime]
    created_at: datetime

class ResultVote(BaseModel):
    """Define the information of the voting result given the specified poll."""
    count: int
    option: Option

class Result(BaseModel):
    """Define the result model of a poll."""
    poll: ResultPoll
    total_votes: int
    votes: List[ResultVote]
