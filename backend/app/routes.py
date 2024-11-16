from flask import Blueprint
from app.controllers import get_invitations_controller, create_invitation_controller

bp = Blueprint('invitations', __name__)

bp.route('/invitations', methods=['GET'])(get_invitations_controller)
bp.route('/invitations', methods=['POST'])(create_invitation_controller)