from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    inactive: Optional[bool] = None   # optional update


class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    description: Optional[str]

    # BaseModel inherited fields
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_by: Optional[str]
    modified_by: Optional[str]
    inactive: bool

    class Config:
        from_attributes = True
