from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.branch_schema import BranchCreate, BranchUpdate, BranchResponse
from app.models.branch_m import Branch
from app.models.user_m import User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(
    branch: BranchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_branch = Branch(**branch.dict(), created_by=current_user.username)
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch

@router.get("/", response_model=List[BranchResponse])
async def get_branches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    branches = db.query(Branch).filter(
        Branch.organization_id == current_user.organization_id,
        Branch.inactive == False
    ).offset(skip).limit(limit).all()
    return branches

@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    branch = db.query(Branch).filter(
        Branch.id == branch_id,
        Branch.organization_id == current_user.organization_id,
        Branch.inactive == False
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@router.put("/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: int,
    branch_update: BranchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    branch = db.query(Branch).filter(
        Branch.id == branch_id,
        Branch.organization_id == current_user.organization_id
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    for key, value in branch_update.dict(exclude_unset=True).items():
        setattr(branch, key, value)
    
    branch.modified_by = current_user.username
    db.commit()
    db.refresh(branch)
    return branch

@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    branch = db.query(Branch).filter(
        Branch.id == branch_id,
        Branch.organization_id == current_user.organization_id
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    branch.inactive = True
    branch.modified_by = current_user.username
    db.commit()
    return {"message": "Branch deleted successfully"}