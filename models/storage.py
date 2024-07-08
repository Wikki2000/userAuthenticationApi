#!/usr/bin/python3
"""Defines storage system using PostgreSQL."""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import environ

class Storage:
    """This models the database system using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        from models.base_model import BaseModel, Base

        """Create session engine for interacting with database."""
        username = environ.get("APP_USER")
        password = environ.get("APP_PASSWORD")
        database = environ.get("APP_DATABASE")
        host = environ.get("APP_HOST", "localhost")  # Default to localhost if not set

        # Ensure all necessary environment variables are set
        if not username or not password or not database:
            raise ValueError("APP_USER, APP_PASSWORD, and APP_DATABASE environment variables must be set")

        # Adjust the engine URL for PostgreSQL
        self.__engine = create_engine(f"postgresql://{username}:{password}@{host}:5432/{database}", pool_pre_ping=True)

        # Create tables if they do not exist
        Base.metadata.create_all(self.__engine)

        # Bind Session to engine
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """Add object to session.new"""
        self.__session.add(obj)

    def save(self):
        """Persist save change to database and add object to session."""
        self.__session.commit()

    def close(self):
        """Close the session after transaction"""
        self.__session.remove()

    def get_session(self):
        """Return the current session."""
        return self.__session

    def drop_all(self):
        from models.base_model import Base
        """Delete all mapped table."""
        Base.metadata.drop_all(self.__engine)
