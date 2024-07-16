import secrets
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import Event, UserModel, RegistrationModel
from app.database import get_db
from app.schemas import EventCreate, EventOut, LoginUser, Registration, RegistrationCreate, User, UserCreate, Token, UserUpdate
from .utils import decode_access_token, verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List
from .database import SessionLocal
from . import schemas, crud, models


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user-info", response_model=User)
def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

@router.put("/updateUser", response_model=User)
def update_user(user_update: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user

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
    owner = db.query(UserModel).filter(UserModel.id == event_data.owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{event_data.owner_id}' not found"
        )
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        owner_id=event_data.owner_id,
        image=event_data.image,
        max_capacity=event_data.max_capacity
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    # Obtener el nombre de usuario del propietario
    owner_username = get_owner_username(db, new_event.owner_id)
    
    return EventOut(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        date=new_event.date,
        owner_username=owner_username,
        owner_id=new_event.owner_id,
        image=new_event.image,
        max_capacity=new_event.max_capacity
    )

def get_owner_username(db: Session, owner_id: int) -> str:
    owner = db.query(UserModel).filter(UserModel.id == owner_id).first()
    if owner:
        return owner.username
    return ""

@router.get("/events/", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    event_out_list = []
    for event in events:
        owner_username = get_owner_username(db, event.owner_id)
        event_out = EventOut(
            id=event.id,
            title=event.title,
            description=event.description,
            date=event.date,
            owner_username=owner_username,
            owner_id=event.owner_id,
            image=event.image,
            max_capacity=event.max_capacity
        )
        event_out_list.append(event_out)
    
    return event_out_list

@router.post("/events/{event_id}/register", response_model=schemas.Registration)
def register_for_event(
    event_id: int,
    registration_data: schemas.RegistrationCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe una inscripción para este usuario y evento
    existing_registration = crud.get_registration_by_user_event(
        db, user_id=registration_data.user_id, event_id=event_id
    )
    if existing_registration:
        raise HTTPException(status_code=400, detail="User is already registered for this event")

    # Verificar la capacidad del evento
    event = crud.get_event(db, event_id=event_id)
    registrations_count = crud.get_registrations_count_by_event(db, event_id=event_id)
    if registrations_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event capacity reached")

    # Si no existe, proceder con la creación de la inscripción
    db_registration = crud.create_registration(db, event_id=event_id, user_id=registration_data.user_id)
    return db_registration

@router.get("/events/{event_id}/registrations", response_model=list[schemas.RegistrationWithUser])
def list_registrations(event_id: int, db: Session = Depends(get_db)):
    registrations = crud.get_registrations_by_event(db, event_id=event_id)
    for registration in registrations:
        registration.user = db.query(models.UserModel).filter(models.UserModel.id == registration.user_id).first()
    return registrations