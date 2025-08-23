"""A module to define the choice model."""

from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Choice(BaseModel):
    """A whole schema of the choice model."""
    id: UUID = Field(default_factory=uuid4)
    description: str = Field(min_length=1, max_length=100)
