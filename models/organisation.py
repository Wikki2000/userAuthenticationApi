from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from models.user_organisation import user_organisation

class Organisation(BaseModel, Base):
    """Class models of user organisation table."""

    __tablename__ = "organisations"

    orgId = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid4()), name="orgId")
    name = Column(String(30), nullable=False)
    description = Column(String(500))

    users = relationship("User", secondary=user_organisation, back_populates="organisations")
