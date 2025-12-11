from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from app.services.event_service import get_all, get_by_id, create, update, delete
from app.database import get_db
from app.dependencies import get_current_user  # ADD THIS

router = APIRouter(prefix="/api/events", tags=["Events"])


# ---------------------------
# LIST EVENTS
# ---------------------------
@router.get("/", response_model=list[EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all(db, user_id=current_user.id)


# ---------------------------
# GET EVENT BY ID
# ---------------------------
@router.get("/{id}", response_model=EventResponse)
def get_event(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = get_by_id(db, id, user_id=current_user.id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


# ---------------------------
# CREATE EVENT
# ---------------------------
@router.post("/", response_model=EventResponse)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create(db, payload, user_id=current_user.id)


# ---------------------------
# UPDATE EVENT
# ---------------------------
@router.put("/{id}", response_model=EventResponse)
def update_event(
    id: int,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = update(db, id, payload, user_id=current_user.id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


# ---------------------------
# DELETE EVENT
# ---------------------------
@router.delete("/{id}")
def delete_event_route(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = delete(db, id, user_id=current_user.id)
    if not result:
        raise HTTPException(404, "Event not found")
    return {"message": "Deleted"}
