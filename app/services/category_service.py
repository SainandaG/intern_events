from sqlalchemy.orm import Session
from app.models.category_m import Category


def get_all(db: Session):
    return db.query(Category).all()


def get_by_id(db: Session, id: int):
    return db.query(Category).filter(Category.id == id).first()


def create(db: Session, data):
    category = Category(**data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, id: int, data):
    category = get_by_id(db, id)
    if not category:
        return None

    for field, value in data.dict(exclude_none=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, id: int):
    category = get_by_id(db, id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False
