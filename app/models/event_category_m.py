from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class EventCategory(BaseModel):
    __tablename__ = "event_categories"

    event_id = Column(Integer, ForeignKey("events.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    event = relationship("Event", back_populates="categories")
    category = relationship("Category", back_populates="events")
