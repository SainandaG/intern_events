from datetime import datetime
from sqlalchemy.orm import Session

from app.models.event_m import Event
from app.models.event_category_m import EventCategory
from app.schemas.event_schema import EventCreate, EventUpdate


def get_all(db: Session, user_id: int):
    return db.query(Event).all()


def get_by_id(db: Session, event_id: int, user_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create(db: Session, payload: EventCreate, user_id: int):
    data = payload.dict(exclude={"category_ids"})
    category_ids = payload.category_ids or []

    # BaseModel fields
    data["created_by"] = user_id
    data["modified_by"] = user_id
    data["created_at"] = datetime.utcnow()
    data["modified_at"] = datetime.utcnow()

    event = Event(**data)
    db.add(event)
    db.commit()
    db.refresh(event)

    # Handle event-category mapping
    for cid in category_ids:
        db.add(EventCategory(event_id=event.id, category_id=cid))

    db.commit()
    db.refresh(event)
    return event


def update(db: Session, event_id: int, payload: EventUpdate, user_id: int):
    event = get_by_id(db, event_id, user_id)
    if not event:
        return None

    data = payload.dict(exclude={"category_ids"}, exclude_unset=True)
    category_ids = payload.category_ids

    # Update event normal fields
    for key, value in data.items():
        setattr(event, key, value)

    # Update base model fields
    event.modified_by = user_id
    event.modified_at = datetime.utcnow()

    db.commit()

    # Update categories if provided
    if category_ids is not None:
        # Remove old categories
        db.query(EventCategory).filter(EventCategory.event_id == event_id).delete()

        # Add new ones
        for cid in category_ids:
            db.add(EventCategory(event_id=event_id, category_id=cid))

        db.commit()

    db.refresh(event)
    return event


def delete(db: Session, event_id: int, user_id: int):
    event = get_by_id(db, event_id, user_id)
    if not event:
        return None

    db.delete(event)
    db.commit()
    return True
