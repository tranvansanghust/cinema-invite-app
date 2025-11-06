from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..models.invitation import Invitation
 
def retrieve_all_invitations(db, skip: int = 0, limit: int = 100) -> list[Invitation]:
    """
    Retrieve all invitations from the database with pagination.
    Compatible with MySQL.
    """
    try:
        stmt = select(Invitation).offset(skip).limit(limit)
        result = db.execute(stmt)
        invitations = result.scalars().all()
        return invitations
    except IntegrityError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e

