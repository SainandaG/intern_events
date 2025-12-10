# app/models/vendor_bid_m.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class VendorBid(BaseModel):
    __tablename__ = "vendor_bids"

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)

    event_id = Column(Integer, nullable=True)  # connect later to events table

    category_id = Column(Integer, nullable=True)  # optional now

    amount = Column(Float, nullable=False)

    status = Column(String(50), default="pending")  
    # pending, submitted, rejected, accepted, cancelled

    notes = Column(String(500), nullable=True)

    submitted_at = Column(DateTime, nullable=True)
    accepted_at = Column(DateTime, nullable=True)

    vendor = relationship("Vendor", back_populates="bids")
