from sqlalchemy import Column, String, ForeignKey, Table
from models.base_model import Base

user_organisation = Table('user_organisation', Base.metadata,
    Column('user_id', String(36), ForeignKey('users.userId'), primary_key=True),
    Column('organisation_id', String(36), ForeignKey('organisations.orgId'), primary_key=True)
)
