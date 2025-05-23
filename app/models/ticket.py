from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String)
    departure = Column(String)
    destination = Column(String)
    date = Column(DateTime)
    price = Column(Float)