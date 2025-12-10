from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import Base


class VendorCategory(Base):
    __tablename__ = "vendor_categories"

    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    vendor = relationship("Vendor", back_populates="categories_link")
    category = relationship("Category", back_populates="vendors")


# IMPORTANT bottom imports:
from .vendor_m import Vendor
from .category_m import Category
