
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    invitations = relationship("Invitation", back_populates="user")
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)