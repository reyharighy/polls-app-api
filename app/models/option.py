"""A module to define the option model."""

from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class OptionCreate(BaseModel):
    """Input definition to create a new option."""
    description: str = Field(min_length=1, max_length=100)

    def create(self) -> 'Option':
        """Instantiate the option model when creating a poll from POST /polls/create endpoint."""
        return Option(description=self.description)

class Option(BaseModel):
    """A whole schema of the option model."""
    id: UUID = Field(default_factory=uuid4)
    description: str
