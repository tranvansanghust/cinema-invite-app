
from app.models import db, Invitation

def create_invitation(data):
    new_invitation = Invitation(
        movie_title=data['movieTitle'],
        date=data['date'],
        location=data['location']
    )
    db.session.add(new_invitation)
    db.session.commit()
    return new_invitation