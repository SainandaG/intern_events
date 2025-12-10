from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return create(db, payload)


@router.get("/{id}", response_model=CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    category = get_by_id(db, id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@router.put("/{id}", response_model=CategoryResponse)
def update_category(id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    return update(db, id, payload)


@router.delete("/{id}")
def delete_category_route(id: int, db: Session = Depends(get_db)):
    delete(db, id)
    return {"message": "Deleted"}
