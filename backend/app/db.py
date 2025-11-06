"""
Legacy database initialization file.
This file is kept for backward compatibility but the actual database
connection is now handled in app.database module.
"""

from app.models import Base
from app.database import engine

async def init_db():
    """
    Initialize database - create all tables.
    Note: In production, use Alembic migrations instead.
    """
    # Import all models to ensure they're registered
    from app.models.user import User
    from app.models.movie import Movie
    from app.models.invitation import Invitation
    
    # Create all tables
    # Note: This is only for development. Use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)