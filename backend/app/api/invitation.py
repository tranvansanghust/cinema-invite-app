from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import invitation as invitation_crud
from ..database import get_db
from ..schemas.invitation import InvitationCreate
from ..models.invitation import Invitation

router = APIRouter()

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
    for key, value in updated_invitation.dict().items():
        setattr(invitation, key, value)
    db.commit()
    db.refresh(invitation)
    return invitation

@router.post("/invitations/add", response_model=InvitationCreate, tags=["Invitations"])
def create_invitation(invitation: InvitationCreate, db: Session = Depends(get_db)):
    try:
        db_invitation = Invitation(
            userid=invitation.userid,
            movieid=invitation.movieid,
            text=invitation.text,
            image_urls=";".join(invitation.image_urls),
            cinema_ids=";".join(invitation.cinema_ids),
            status=invitation.status,
            amount_of_reach=invitation.amount_of_reach,
        )
        db.add(db_invitation)
        db.commit()
        db.refresh(db_invitation)
        return invitation
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create invitation")
    finally:
        db.close()
    
@router.get("/invitations/", response_model=List[InvitationCreate], tags=["Invitations"])
def get_invitations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        invitations = invitation_crud.retrieve_all_invitations(db, skip=skip, limit=limit)
        res = []
        for invitation in invitations:
            print(invitation)
            res.append(invitation)

        return res

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve invitations" + str(e))
    finally:
        db.close()