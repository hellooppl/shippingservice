from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    pass


class NotAvailable(Event):
    user: UUID
