from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BranchBase(BaseModel):
    name: str
    code: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None

class BranchCreate(BranchBase):
    organization_id: int
    is_head_office: Optional[int] = 0

class BranchUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class BranchResponse(BranchBase):
    id: int
    organization_id: int
    is_head_office: int
    created_at: datetime
    
    class Config:
        from_attributes = True