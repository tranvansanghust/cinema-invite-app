import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_sso.sso.google import GoogleSSO
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.database import get_db
from app.crud.user import create_user, get_user, authenticate_user
from app.utils.auth import create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_sso = GoogleSSO(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    allow_insecure_http=True
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/token", tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with username (email) and password to get JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserSchema.from_orm(user)
    }

@router.post("/register", response_model=UserSchema, tags=["Authentication"])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db=db, user=user)

@router.get("/login/google", tags=["Google SSO"])
async def google_login():
    """Start Google OAuth flow."""
    with google_sso:
        redirect_url = await google_sso.get_login_redirect(
            params={"prompt": "consent", "access_type": "offline"}
        )
        return redirect_url

@router.get("/login/google/callback", tags=["Google SSO"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Process Google OAuth callback and return JWT token."""
    try:
        async with google_sso:
            user_info = await google_sso.verify_and_process(request)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        user_info = user_info.dict()
        user = get_user(db=db, email=user_info["email"])
        
        # Create user if not exists
        if user is None:
            user_create = UserCreate(
                email=user_info["email"],
                name=user_info["display_name"],
                password=os.urandom(32).hex()  # Random secure password for OAuth users
            )
            user = create_user(db=db, user=user_create)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Redirect to frontend with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(
            url=f"{frontend_url}/callback?token={access_token}",
            status_code=status.HTTP_302_FOUND
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {str(e)}"
        )

@router.get("/me", response_model=UserSchema, tags=["Authentication"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info."""
    return current_user.__dict__
