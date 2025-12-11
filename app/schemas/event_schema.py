from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class EventBase(BaseModel):
    title: str
    location: Optional[str] = None
    city: Optional[str] = None
    venue: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class EventCreate(EventBase):
    category_ids: Optional[List[int]] = []


class EventUpdate(EventBase):
    category_ids: Optional[List[int]] = []


class EventResponse(EventBase):
    id: int

    # 🔥 Added fields from extended BaseModel
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    inactive: Optional[bool] = None

    class Config:
        from_attributes = True
