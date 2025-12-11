from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.role_right_m import RoleRight
from app.models.user_m import User
from app.dependencies import get_current_active_user, PermissionChecker
from app.services.permission_sync_service import PermissionSyncService

router = APIRouter(prefix="/role-rights", tags=["Role Rights"])

class RoleRightCreate(BaseModel):
    role_id: int
    menu_id: int
    can_view: bool = True
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False

class RoleRightUpdate(BaseModel):
    can_view: bool = True
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False

@router.post(
    "/",
    dependencies=[Depends(PermissionChecker(["role.manage"]))]
)
async def create_role_right(
    data: RoleRightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if already exists
    existing = db.query(RoleRight).filter(
        RoleRight.role_id == data.role_id,
        RoleRight.menu_id == data.menu_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Role right already exists")
    
    # Create role_right
    role_right = RoleRight(
        role_id=data.role_id,
        menu_id=data.menu_id,
        can_view=data.can_view,
        can_create=data.can_create,
        can_edit=data.can_edit,
        can_delete=data.can_delete,
        created_by=current_user.username
    )
    
    db.add(role_right)
    db.flush()
    
    # 🔄 AUTO-SYNC: Update role_permissions
    PermissionSyncService.sync_role_permissions(
        db, data.role_id, data.menu_id, role_right
    )
    
    db.commit()
    
    return {"message": "Role right created and permissions synced"}

@router.put(
    "/{role_right_id}",
    dependencies=[Depends(PermissionChecker(["role.manage"]))]
)
async def update_role_right(
    role_right_id: int,
    data: RoleRightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    role_right = db.query(RoleRight).filter(
        RoleRight.id == role_right_id
    ).first()
    
    if not role_right:
        raise HTTPException(status_code=404, detail="Role right not found")
    
    # Update fields
    role_right.can_view = data.can_view
    role_right.can_create = data.can_create
    role_right.can_edit = data.can_edit
    role_right.can_delete = data.can_delete
    role_right.modified_by = current_user.username
    
    db.flush()
    
    # 🔄 AUTO-SYNC: Update role_permissions
    PermissionSyncService.sync_role_permissions(
        db, role_right.role_id, role_right.menu_id, role_right
    )
    
    db.commit()
    
    return {"message": "Role right updated and permissions synced"}

@router.get("/{role_id}")
async def get_role_rights(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    role_rights = db.query(RoleRight).filter(
        RoleRight.role_id == role_id,
        RoleRight.inactive == False
    ).all()
    
    return [{
        "id": rr.id,
        "menu_id": rr.menu_id,
        "can_view": rr.can_view,
        "can_create": rr.can_create,
        "can_edit": rr.can_edit,
        "can_delete": rr.can_delete
    } for rr in role_rights]