from sqlalchemy.orm import Session
from datetime import datetime
from app.models.category_m import Category


def get_all(db: Session):
    """Return only active categories (not soft deleted)."""
    return db.query(Category).filter(Category.inactive == False).all()


def get_by_id(db: Session, id: int):
    return db.query(Category).filter(Category.id == id, Category.inactive == False).first()


def create(db: Session, data, user=None):
    payload = data.dict()

    # optional: set created_by
    if user:
        payload["created_by"] = user

    category = Category(**payload)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, id: int, data, user=None):
    category = get_by_id(db, id)
    if not category:
        return None

    for field, value in data.dict(exclude_none=True).items():
        setattr(category, field, value)

    # optional: track modifier
    if user:
        category.modified_by = user

    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, id: int, user=None):
    """Soft delete instead of hard delete."""
    category = get_by_id(db, id)
    if not category:
        return False

    category.inactive = True
    category.deleted_at = datetime.utcnow()
    if user:
        category.modified_by = user

    db.commit()
    return True
