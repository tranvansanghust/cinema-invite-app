from pydantic import BaseModel
from typing import List, Optional

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

    class Config:
        orm_mode = True