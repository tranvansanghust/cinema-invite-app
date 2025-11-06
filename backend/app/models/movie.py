from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), index=True, nullable=False)
    invitations = relationship("Invitation", back_populates="movie")
    description = Column(Text, nullable=True)
    release_date = Column(String(32), nullable=True)
    genre = Column(String(64), nullable=True)
    director = Column(String(128), nullable=True)
    actors = Column(String(255), nullable=True)
    