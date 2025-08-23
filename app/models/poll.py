"""A module to define the poll model."""

from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from pytz import timezone

# Intra-package imports
from .choice import Choice

class PollCreate(BaseModel):
    """Input definition to create a new poll model."""
    title: str = Field(min_length=1, max_length=100)
    options: List[str]
    expires_at: Optional[datetime] = None

    @field_validator("options")
    @classmethod
    def validate_options(cls, options):
        """Validate if the options are between 2 and 5 in total."""
        if len(options) < 2 or len(options) > 5:
            raise ValueError("The options should only be between 2 and 5")

        return options

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, expires_at):
        """Validate if the expired date is in the future if provided."""
        if expires_at and expires_at < datetime.now(timezone('Asia/Jakarta')):
            raise ValueError("Expired date should be set in the future")

        return expires_at

    def create(self) -> 'Poll':
        """Instantiate the poll model from POST /polls/create endpoint."""
        choice = [Choice(description=description) for description in self.options]

        return Poll(
            title=self.title,
            options=choice,
            expires_at=self.expires_at
        )

class Poll(PollCreate):
    """A whole schema of the poll model."""
    id: UUID = Field(default_factory=uuid4)
    options: List[Choice] # type: ignore[override]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone('Asia/Jakarta')))
