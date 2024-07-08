#!/usr/bin/python3
"""
<base_module>: Models the base class for the user_authentication application.
"""
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel:
    """Defines common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Create instance of base model.

        Args:
            args: Won't be used.
            kwargs: The attributes that will be instantiated.
        """
        self.__dict__.update(**kwargs)

    def save(self):
        """Save an instance to the database."""
        models.storage.new(self)
        models.storage.save()

    def get_session(self):
        """Get the database session engine.

        Returns: The session engine.
        """
        session = models.storage.get_session()
        return session

    @classmethod
    def get_user_email(cls, email):
        """fetch a user by email.

        args:
            email (string): the id of the user to retrieve.

        returns:
            user object if found, else none.
        """
        session = models.storage.get_session()
        try:
            user = session.query(cls).filter_by(email=email)
            return user
        except noresultfound:
            return none

    def __str__(self):
        """Display an object in a human-readable form.

        Returns: The string representation of the object.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
