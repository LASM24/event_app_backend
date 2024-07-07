# backend/app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'r6a7?qk):$8M3@wK,&v~CQ'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://db_admin:35ue2iM6UHTdfp97jv8pihWoKBLeTtsK@dpg-cq4vhqdds78s73cq96ig-a.oregon-postgres.render.com/events_web_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'r6a7?qk):$8M3@wK,&v~CQ'
