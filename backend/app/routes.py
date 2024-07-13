import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Event, UserModel, RegistrationModel
from app.database import get_db
from app.schemas import EventCreate, EventOut, LoginUser, Registration, RegistrationCreate, User, UserCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/user-register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=User)
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return db_user

# crear eventos
@router.post("/events-create", response_model=EventOut)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    # Buscar al usuario por nombre de usuario
    owner = db.query(UserModel).filter(UserModel.username == event_data.owner_username).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{event_data.owner_username}' not found"
        )
    
    # Crear el evento asociado al propietario encontrado usando owner.username
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        owner_username=event_data.owner_username,
        image= event_data.image,
        max_capacity= event_data.max_capacity
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    # Devolver el evento creado como respuesta, asegurándote de incluir owner_username
    return EventOut(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        date=new_event.date,
        owner_username=new_event.owner_username,
        image= event_data.image,
        max_capacity= event_data.max_capacity
    )

@router.get("/events", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events


# Registrarse en un evento
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

