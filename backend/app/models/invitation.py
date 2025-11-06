from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

from app.utils.parser import parse_string_to_array

class Invitation(Base):
    __tablename__ = "invitations"

    invitationid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    movieid = Column(Integer, ForeignKey("movies.id"), nullable=False)
    text = Column(Text, nullable=True)
    # MySQL doesn't support ARRAY, so we use TEXT and parse it
    image_urls = Column(Text, nullable=True)  # Stored as semicolon-separated string
    cinema_ids = Column(Text, nullable=True)  # Stored as semicolon-separated string
    status = Column(String(255), nullable=True)
    amount_of_reach = Column(Integer, nullable=True, default=0)

    user = relationship("User", back_populates="invitations")
    movie = relationship("Movie", back_populates="invitations")
    
    def parse_fields(self):
        """
        Parses string fields (image_urls, cinema_ids) into arrays.
        """
        self.image_urls = parse_string_to_array(self.image_urls)
        self.cinema_ids = parse_string_to_array(self.cinema_ids)
