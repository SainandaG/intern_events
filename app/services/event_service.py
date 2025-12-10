from sqlalchemy.orm import Session
from app.models.event_m import Event
from app.schemas.event_schema import EventCreate, EventUpdate


def get_all(db: Session):
    return db.query(Event).all()


def get_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create(db: Session, payload: EventCreate):
    event = Event(**payload.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update(db: Session, event_id: int, payload: EventUpdate):
    event = get_by_id(db, event_id)
    if not event:
        return None

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event


def delete(db: Session, event_id: int):
    event = get_by_id(db, event_id)
    if not event:
        return None
    
    db.delete(event)
    db.commit()
    return True
