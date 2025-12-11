from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


# ---------------------------
# Base Schema (Input + Shared)
# ---------------------------
class VendorProfileBase(BaseModel):
    company_name: str
    business_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    website: Optional[str] = None

    categories: Optional[List[str]] = None
    service_areas: Optional[List[str]] = None
    year_established: Optional[str] = None
    team_size: Optional[str] = None

    license_number: Optional[str] = None
    insurance_provider: Optional[str] = None
    tax_id: Optional[str] = None

    description: Optional[str] = None
    status: Optional[str] = None


# ---------------------------
# Update Schema
# ---------------------------
class VendorProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    business_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    website: Optional[str] = None

    categories: Optional[List[str]] = None
    service_areas: Optional[List[str]] = None
    year_established: Optional[str] = None
    team_size: Optional[str] = None

    license_number: Optional[str] = None
    insurance_provider: Optional[str] = None
    tax_id: Optional[str] = None

    description: Optional[str] = None
    status: Optional[str] = None


# ---------------------------
# Response Schema (Includes BaseModel fields)
# ---------------------------
class VendorProfileResponse(VendorProfileBase):
    id: int
    user_id: int

    # BaseModel extended fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    inactive: Optional[bool] = None

    created_by: Optional[str] = None
    modified_by: Optional[str] = None

    class Config:
        from_attributes = True
