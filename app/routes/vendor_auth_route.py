# app/routes/vendor_auth_route.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_m import User
from app.models.role_m import Role
from app.models.vendor_m import Vendor
from app.schemas.vendor_auth_schema import (
    VendorRegisterRequest,
    VendorLoginRequest,
    VendorAuthResponse,
    VendorAuthUser,
)
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token


router = APIRouter(prefix="/auth/vendor", tags=["Vendor Auth"])


def get_vendor_role(db: Session) -> Role:
    role = db.query(Role).filter(Role.code == "VENDOR").first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Vendor role not configured in system",
        )
    return role


@router.post("/register", response_model=VendorAuthResponse)
def register_vendor(payload: VendorRegisterRequest, db: Session = Depends(get_db)):
    # Check email already exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    vendor_role = get_vendor_role(db)

    username = payload.email.split("@")[0]

    user = User(
        username=username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role_id=vendor_role.id,
        created_by="vendor_self",
    )
    db.add(user)
    db.flush()

    # Create Vendor profile
    vendor = Vendor(
        user_id=user.id,
        company_name=payload.company_name,
        business_type=payload.business_type,
        phone=payload.phone,
        address=payload.address,
        city=payload.city,
        state=payload.state,
        zip_code=payload.zip_code,
        status="pending",
    )
    db.add(vendor)
    db.commit()
    db.refresh(user)

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
    }
    access_token = create_access_token(token_data)

    return VendorAuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=VendorAuthUser.model_validate(user),
    )


@router.post("/login", response_model=VendorAuthResponse)
def login_vendor(payload: VendorLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Ensure user is vendor
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role or role.code != "VENDOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a vendor account",
        )

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
    }
    access_token = create_access_token(token_data)

    return VendorAuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=VendorAuthUser.model_validate(user),
    )
