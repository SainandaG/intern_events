from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from app.services.event_service import get_all, get_by_id, create, update, delete
from app.database import get_db

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("/", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{id}", response_model=EventResponse)
def get_event(id: int, db: Session = Depends(get_db)):
    event = get_by_id(db, id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


@router.post("/", response_model=EventResponse)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    return create(db, payload, user_id=1)  # TODO replace with admin user


@router.put("/{id}", response_model=EventResponse)
def update_event(id: int, payload: EventUpdate, db: Session = Depends(get_db)):
    event = update(db, id, payload)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


@router.delete("/{id}")
def delete_event_route(id: int, db: Session = Depends(get_db)):
    result = delete(db, id)
    if not result:
        raise HTTPException(404, "Event not found")
    return {"message": "Deleted"}
