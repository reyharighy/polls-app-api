"""A module to define the poll model."""

from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

# Intra-package imports
from .option import OptionCreate, Option

class PollCreate(BaseModel):
    """Input definition to create a new poll model."""
    title: str = Field(min_length=1, max_length=100)
    options: List[str] = Field(min_length=2, max_length=5)
    expires_at: Optional[datetime] = None

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, expires_at):
        """Validate the expires_at should be in the future if provided."""
        if expires_at and expires_at < datetime.now():
            raise ValueError("expired time should be set in the future")

        return expires_at

    def create(self) -> 'Poll':
        """Instantiate the poll model from POST /polls/create endpoint."""
        options = [
            OptionCreate(description=description).create()
            for description in self.options
        ]

        return Poll(
            title=self.title,
            options=options,
            expires_at=self.expires_at
        )

class Poll(BaseModel):
    """A whole schema of the poll model."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    options: List[Option]
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
