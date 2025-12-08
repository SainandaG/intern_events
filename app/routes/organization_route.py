from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.organization_schema import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.models.organization_m import Organization
from app.models.user_m import User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_org = db.query(Organization).filter(Organization.code == org.code).first()
    if db_org:
        raise HTTPException(status_code=400, detail="Organization code already exists")
    
    new_org = Organization(**org.dict(), created_by=current_user.username)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    orgs = db.query(Organization).filter(Organization.inactive == False).offset(skip).limit(limit).all()
    return orgs

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    org = db.query(Organization).filter(Organization.id == org_id, Organization.inactive == False).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    for key, value in org_update.dict(exclude_unset=True).items():
        setattr(org, key, value)
    
    org.modified_by = current_user.username
    db.commit()
    db.refresh(org)
    return org

@router.delete("/{org_id}")
async def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    org.inactive = True
    org.modified_by = current_user.username
    db.commit()
    return {"message": "Organization deleted successfully"}