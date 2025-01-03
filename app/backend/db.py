# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import Column, Integer, String

engine = create_engine("sqlite:///taskmanager.db")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

