import secrets
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Event, UserModel, RegistrationModel
from app.database import get_db
from app.schemas import EventCreate, EventOut, LoginUser, Registration, RegistrationCreate, User, UserCreate, Token
from .utils import verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/user-register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Crear eventos
@router.post("/events-create", response_model=EventOut)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    owner = db.query(UserModel).filter(UserModel.username == event_data.owner_username).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{event_data.owner_username}' not found"
        )
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        owner_username=event_data.owner_username,
        image=event_data.image,
        max_capacity=event_data.max_capacity
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return EventOut(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        date=new_event.date,
        owner_username=new_event.owner_username,
        image=event_data.image,
        max_capacity=event_data.max_capacity
    )

@router.get("/events", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@router.post("/events/{event_id}/register", response_model=Registration)
def register_for_event(
    registration_data: RegistrationCreate, 
    db: Session = Depends(get_db)
):
    db_registration = RegistrationModel(
        event_id=registration_data.event_id,
        user_id=registration_data.user_id
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

@router.get("/events/{event_id}/registrations", response_model=list[Registration])
def list_registrations(event_id: int, db: Session = Depends(get_db)):
    registrations = db.query(RegistrationModel).filter(RegistrationModel.event_id == event_id).all()
    return registrations
