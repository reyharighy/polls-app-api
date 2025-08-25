"""A module to define the vote model."""

from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
from pytz import timezone

# Intra-package imports
from .poll import Poll

class Voter(BaseModel):
    """A whole schema of the voter model."""
    email: EmailStr

class VoteCreate(BaseModel):
    """Input definition to create a new vote."""
    option_id: UUID
    voter: Voter

    def create(self, poll: Poll, option_description: str) -> 'Vote':
        """Instantiate the vote model from POST votes/{poll_id}/create endpoint."""
        return Vote(
            poll=VotePoll(
                id=poll.id,
                title=poll.title
            ),
            option=VoteOption(
                id=self.option_id,
                description=option_description
            ),
            voter=self.voter
        )

class VotePoll(BaseModel):
    """Define the nested poll model when voted."""
    id: UUID
    title: str

class VoteOption(BaseModel):
    """Define the nested option model when voted."""
    id: UUID
    description: str

class Vote(BaseModel):
    """A whole schema of the vote model."""
    id: UUID = Field(default_factory=uuid4)
    poll: VotePoll
    option: VoteOption
    voter: Voter
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone('Asia/Jakarta')))
