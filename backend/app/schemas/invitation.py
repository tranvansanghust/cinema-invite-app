from pydantic import BaseModel, validator
from typing import List, Optional, Union
from app.utils.parser import parse_string_to_array

class InvitationBase(BaseModel):
    userid: int
    movieid: int
    text: Optional[str] = None
    image_urls: Optional[List[str]] = None
    cinema_ids: Optional[List[int]] = None
    status: Optional[str] = None
    amount_of_reach: Optional[int] = None

class InvitationCreate(InvitationBase):
    pass

class Invitation(InvitationBase):
    invitationid: int

    @validator('image_urls', pre=True)
    def parse_image_urls(cls, v):
        """Convert semicolon-separated string to list."""
        if isinstance(v, str):
            return parse_string_to_array(v)
        return v
    
    @validator('cinema_ids', pre=True)
    def parse_cinema_ids(cls, v):
        """Convert semicolon-separated string to list of integers."""
        if isinstance(v, str):
            arr = parse_string_to_array(v)
            return [int(x) for x in arr if x.strip()] if arr else []
        return v

    class Config:
        orm_mode = True