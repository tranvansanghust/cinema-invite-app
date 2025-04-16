from sqlalchemy import Column, Integer, String, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from app.models.base import Base

class Invitation(Base):
    __tablename__ = "invitations"

    invitationid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    movieid = Column(Integer, ForeignKey("movies.id"), nullable=False)
    text = Column(Text, nullable=True)
    image_urls = Column(ARRAY(String), nullable=True)
    cinema_ids = Column(ARRAY(Integer), nullable=True)
    status = Column(String, nullable=True)
    amount_of_reach = Column(Integer, nullable=True)

    user = relationship("User", back_populates="invitations")
    movie = relationship("Movie", back_populates="invitations")