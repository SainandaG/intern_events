# app/schemas/vendor_auth_schema.py

from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import Annotated



class VendorRegisterRequest(BaseModel):
    # Account info
    email: EmailStr
    password: Annotated[str, 8]

    # Basic vendor info (same as VendorRegister.tsx step 2)
    company_name: str
    business_type: str
    phone: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None


class VendorLoginRequest(BaseModel):
    email: EmailStr
    password: str


class VendorAuthUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: int

    class Config:
        from_attributes = True


class VendorAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: VendorAuthUser
