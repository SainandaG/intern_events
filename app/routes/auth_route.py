from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.models.user_m import User
from app.models.menu_m import Menu
from app.models.role_right_m import RoleRight
from app.utils.password_utils import verify_password
from app.utils.jwt_utils import create_access_token
from app.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    # ---------------------
    # VALIDATE USER
    # ---------------------
    user = db.query(User).filter(
        User.username == request.username,
        User.inactive == False
    ).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # ---------------------
    # GENERATE TOKEN
    # ---------------------
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id,
        },
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    # ---------------------
    # FETCH ROLE MENUS
    # ---------------------
    role_rights = db.query(RoleRight).filter(
        RoleRight.role_id == user.role_id,
        RoleRight.can_view == True
    ).all()

    menu_ids = [rr.menu_id for rr in role_rights]

    menus = db.query(Menu).filter(
        Menu.id.in_(menu_ids),
        Menu.inactive == False
    ).order_by(Menu.sort_order).all()

    # convert menu objects
    menus_out = [{
        "id": m.id,
        "name": m.name,
        "route": m.route,
        "code": m.code,
        "icon": m.icon,
    } for m in menus]

    rights_out = [{
        "menu_id": rr.menu_id,
        "can_view": rr.can_view,
        "can_create": rr.can_create,
        "can_edit": rr.can_edit,
        "can_delete": rr.can_delete,
    } for rr in role_rights]

    # ---------------------
    # RETURN
    # ---------------------
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        },
        "menus": menus_out,
        "rights": rights_out
    }


__all__ = ["router"]
