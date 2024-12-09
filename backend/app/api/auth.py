from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
from dotenv import load_dotenv
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
async def google_callback(request: Request):
    """Process login response from Google and return user info"""

    try:
        async with google_sso:
            user = await google_sso.verify_and_process(request)
        
        print("User info:", user)
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")