from sqlalchemy.orm import Session
from . import models

def get_registration_by_user_event(db: Session, user_id: int, event_id: int):
    return db.query(models.RegistrationModel).filter(
        models.RegistrationModel.user_id == user_id,
        models.RegistrationModel.event_id == event_id
    ).first()

def create_registration(db: Session, event_id: int, user_id: int):
    db_registration = models.RegistrationModel(event_id=event_id, user_id=user_id)
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

def get_registrations_by_event(db: Session, event_id: int):
    return db.query(models.RegistrationModel).filter(models.RegistrationModel.event_id == event_id).all()

def get_registrations_count_by_event(db: Session, event_id: int):
    return db.query(models.RegistrationModel).filter(models.RegistrationModel.event_id == event_id).count()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()
