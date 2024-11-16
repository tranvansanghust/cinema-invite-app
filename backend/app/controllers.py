from flask import jsonify, request
from app.models import Invitation
from app.crud import create_invitation

def get_invitations_controller():
    invitations = [
        {"movieTitle": "Inception", "date": "2023-10-01", "location": "Cinema 1"},
        {"movieTitle": "Interstellar", "date": "2023-10-02", "location": "Cinema 2"}
    ]
    return jsonify(invitations)

def create_invitation_controller():
    data = request.get_json()
    new_invitation = create_invitation(data)
    return jsonify(new_invitation), 201