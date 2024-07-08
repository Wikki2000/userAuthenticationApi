from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from uuid import uuid4
from datetime import datetime
from models.user_organisation import user_organisation

class User(BaseModel, Base):
    """Class models of user data table."""

    __tablename__ = "users"

    userId = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid4()), name="userId")
    firstName = Column(String(30), nullable=False)
    lastName = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(5000), nullable=False)
    phone = Column(String(20))

    organisations = relationship("Organisation", secondary=user_organisation, back_populates="users")

    def hash_password(self, password):
        """Hashes the password before saving."""
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return bcrypt.verify(password, self.password)
