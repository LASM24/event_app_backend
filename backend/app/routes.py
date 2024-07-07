# backend/app/routes.py
from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User, Event, Registration
from .schemas import UserSchema, EventSchema, RegistrationSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

user_schema = UserSchema()
event_schema = EventSchema()
registration_schema = RegistrationSchema()

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad credentials"}), 401

@main.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
   
    if not title or not description or not date:
        return jsonify(message='Missing required fields'), 400
    
    try:
        # Crea un nuevo evento en la base de datos
        new_event = Event(title=title, description=description, date=date)
        db.session.add(new_event)
        db.session.commit()
        return jsonify(message='Event created successfully'), 201
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify(message='Failed to create event'), 500

@main.route('/events', methods=['GET'])
def list_events():
    events = Event.query.all()
    return event_schema.jsonify(events, many=True)

@main.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    user_id = get_jwt_identity()
    new_registration = Registration(event_id=event_id, user_id=user_id)
    db.session.add(new_registration)
    db.session.commit()
    return registration_schema.jsonify(new_registration)

@main.route('/events/<int:event_id>/registrations', methods=['GET'])
@jwt_required()
def list_registrations(event_id):
    user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != user_id:
        return jsonify({"msg": "Permission denied"}), 403
    registrations = Registration.query.filter_by(event_id=event_id).all()
    return registration_schema.jsonify(registrations, many=True)
