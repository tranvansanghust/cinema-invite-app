
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    invitations = relationship("Invitation", back_populates="movie")
    description = Column(String)
    release_date = Column(String)
    genre = Column(String)
    director = Column(String)
    actors = Column(String)
    