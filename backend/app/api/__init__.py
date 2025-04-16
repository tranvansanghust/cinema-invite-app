
from .movie import router as movie_router
from .invitation import router as invitation_router
routers = [movie_router, invitation_router]

# Add invitation routes to the main application
from .invitation import router as invitation_router