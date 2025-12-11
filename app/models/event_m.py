from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Event(BaseModel):
    __tablename__ = "events"

    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    venue = Column(String(255), nullable=True)

    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    description = Column(Text, nullable=True)

    categories = relationship(
    "EventCategory",
    back_populates="event",
    cascade="all, delete-orphan"
)

