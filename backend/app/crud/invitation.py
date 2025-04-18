from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.invitation import Invitation
 
def retrieve_all_invitations(db, skip: int = 0, limit: int = 100) -> list[Invitation]:
    """
    Retrieve all invitations from the database with pagination.
    """

    return db.query(Invitation).offset(skip).limit(limit).all()
