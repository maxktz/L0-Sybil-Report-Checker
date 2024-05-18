import datetime
import random
from typing import Optional

from beanie import Document, Insert, Update, ValidateOnSave, before_event
from pydantic.fields import Field


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


def id_factory(digits: int = 10) -> int:
    return random.randint(10 ** (digits - 1), (10**digits) - 1)


class TimestampedDocument(Document):
    created_at: datetime.datetime = Field(default_factory=utcnow)
    """datetime: Date when document was created."""
    updated_at: datetime.datetime = Field(default_factory=utcnow)
    """datetime: Date when document was updated."""

    @before_event(ValidateOnSave, Update)
    def update_updated_at(self):
        self.updated_at = utcnow()

    @before_event(Insert)
    def create_created_at(self):
        self.created_at = utcnow()


class Report(TimestampedDocument):
    description: Optional[str] = None
