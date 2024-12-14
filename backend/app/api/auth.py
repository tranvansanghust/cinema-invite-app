from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from sqlalchemy.orm import Session
from app.database import get_db
from starlette.requests import Request
from dotenv import load_dotenv

from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user

import os


load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_sso = GoogleSSO(
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    allow_insecure_http=True
)

router = APIRouter()


@router.get("/login/google", tags=['Google SSO'])
async def google_login():
    with google_sso:
        direct_login = await google_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})
        return direct_login


@router.get("/login/google/callback", tags=['Google SSO'])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Process login response from Google and return user info"""

    try:
        async with google_sso:
            user_info = await google_sso.verify_and_process(request)
        
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")
        
        user_info = user_info.dict()
        print("User info:", user_info, user_info["email"])
        user = get_user(db=db, email=user_info["email"])
        # save user info to database
        if user is None:
            print("Creating user...")
            user = UserCreate(
                email=user_info["email"],
                name=user_info["display_name"], 
                password="password"
            )
            create_user(db=db, user=user)
        
        # redirect to home page
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

        return response
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")