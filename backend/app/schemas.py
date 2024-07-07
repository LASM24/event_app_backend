# backend/app/schemas.py
from flask_marshmallow import Marshmallow
from .models import User, Event, Registration

mars = Marshmallow() 

class UserSchema(mars.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        load_only = ("password",)

class EventSchema(mars.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        include_fk = True
        load_instance = True

class RegistrationSchema(mars.SQLAlchemyAutoSchema):
    class Meta:
        model = Registration
        include_fk = True
        load_instance = True
