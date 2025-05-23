from pydantic import BaseModel
from datetime import datetime


class TicketBase(BaseModel):
    flight_number: str
    departure: str
    destination: str
    date: datetime
    price: float


class Ticket(TicketBase):
    id: int

    class Config:
        from_attributes = True