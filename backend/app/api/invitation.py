from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas

from ..crud import invitation as invitation_crud
from ..database import get_db
from ..schemas.invitation import InvitationCreate
from ..models.invitation import Invitation
from logging import getLogger

router = APIRouter()

logger = getLogger(__name__)

@router.get("/invitations/{invitation_id}", response_model=InvitationCreate, tags=["Invitations"])
def get_invitation(invitation_id: int, db: Session = Depends(get_db)):
    invitation = db.query(Invitation).filter(Invitation.invitationid == invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return invitation

@router.delete("/invitations/{invitation_id}", tags=["Invitations"])
def delete_invitation(invitation_id: int, db: Session = Depends(get_db)):
    invitation = db.query(Invitation).filter(Invitation.invitationid == invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    db.delete(invitation)
    db.commit()
    return {"message": "Invitation deleted successfully"}

@router.put("/invitations/{invitation_id}", response_model=InvitationCreate, tags=["Invitations"])
def update_invitation(invitation_id: int, updated_invitation: InvitationCreate, db: Session = Depends(get_db)):
    invitation = db.query(Invitation).filter(Invitation.invitationid == invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Update fields, converting lists to strings for MySQL storage
    update_data = updated_invitation.dict()
    if 'image_urls' in update_data and update_data['image_urls']:
        update_data['image_urls'] = ";".join(update_data['image_urls'])
    if 'cinema_ids' in update_data and update_data['cinema_ids']:
        update_data['cinema_ids'] = ";".join(map(str, update_data['cinema_ids']))
    
    for key, value in update_data.items():
        setattr(invitation, key, value)
    
    db.commit()
    db.refresh(invitation)
    return invitation

@router.post("/invitations/add", response_model=InvitationCreate, tags=["Invitations"])
def create_invitation(invitation: InvitationCreate, db: Session = Depends(get_db)):
    try:
        # Convert lists to semicolon-separated strings for MySQL storage
        image_urls_str = ";".join(invitation.image_urls) if invitation.image_urls else None
        cinema_ids_str = ";".join(map(str, invitation.cinema_ids)) if invitation.cinema_ids else None
        
        db_invitation = Invitation(
            userid=invitation.userid,
            movieid=invitation.movieid,
            text=invitation.text,
            image_urls=image_urls_str,
            cinema_ids=cinema_ids_str,
            status=invitation.status,
            amount_of_reach=invitation.amount_of_reach or 0,
        )
        db.add(db_invitation)
        db.commit()
        db.refresh(db_invitation)
        return invitation
    
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create invitation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create invitation: {str(e)}")
    
@router.get("/invitations/", response_model=List[schemas.Invitation], tags=["Invitations"])
def get_invitations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        invitations = invitation_crud.retrieve_all_invitations(db, skip=skip, limit=limit)
        if not invitations:
            raise HTTPException(status_code=404, detail="No invitations found")
        return invitations

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve invitations: {str(e)}")