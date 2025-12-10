# app/models/vendor_m.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    company_name = Column(String(255), nullable=False)
    business_type = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)

    year_established = Column(String(10), nullable=True)
    team_size = Column(String(50), nullable=True)

    license_number = Column(String(100), nullable=True)
    insurance_provider = Column(String(255), nullable=True)
    tax_id = Column(String(100), nullable=True)

    description = Column(Text, nullable=True)

    status = Column(String(50), nullable=False, default="pending")

    # relationships
    user = relationship("User", back_populates="vendor_profile")

    categories_link = relationship(
        "VendorCategory",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    bids = relationship("VendorBid", back_populates="vendor")
    orders = relationship("VendorOrder", back_populates="vendor")
    payments = relationship("VendorPayment", back_populates="vendor")


# IMPORTANT — Import AFTER class definition
from .vendor_category_m import VendorCategory
from .vendor_bid_m import VendorBid
from .vendor_order_m import VendorOrder
from .vendor_payment_m import VendorPayment
