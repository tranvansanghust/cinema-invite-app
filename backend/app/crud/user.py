from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import get_password_hash, verify_password

def create_user(db: Session, user: UserCreate):
    """Create a new user with hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        name=user.name, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user(db: Session, email: str):
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user with email and password."""
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
