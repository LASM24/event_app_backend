# app/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Event, UserModel, RegistrationModel
from app.database import get_db
from app.schemas import EventCreate, Event, RegistrationCreate, Registration

router = APIRouter()

@router.post("/events-create", response_model=Event)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(title=event_data.title, description=event_data.description, date=event_data.date)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events", response_model=list[Event])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@router.post("/events/{event_id}/register", response_model=Registration)
def register_for_event(event_id: int, registration_data: RegistrationCreate, db: Session = Depends(get_db)):
    db_registration = RegistrationModel(event_id=event_id, user_id=registration_data.user_id)
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

@router.get("/events/{event_id}/registrations", response_model=list[Registration])
def list_registrations(event_id: int, db: Session = Depends(get_db)):
    registrations = db.query(RegistrationModel).filter(RegistrationModel.event_id == event_id).all()
    return registrations
