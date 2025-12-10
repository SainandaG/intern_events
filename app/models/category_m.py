from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base_model import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    icon = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    vendors = relationship(
        "VendorCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    events = relationship(
        "EventCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )


# IMPORTANT – do NOT import models here!
# They are discovered automatically by SQLAlchemy
