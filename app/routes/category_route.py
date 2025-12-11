from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import get_all, get_by_id, create, update, delete

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Return active categories only."""
    return get_all(db)


@router.post("/", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    category = create(db, payload)
    return category


@router.get("/{id}", response_model=CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    category = get_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{id}", response_model=CategoryResponse)
def update_category(id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = update(db, id, payload)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{id}")
def delete_category_route(id: int, db: Session = Depends(get_db)):
    success = delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or already deleted")
    return {"message": "Category soft-deleted successfully"}
