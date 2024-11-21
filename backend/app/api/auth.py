from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth

from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO

# ...existing code...

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth = OAuth()


# ...existing code...
google_sso = GoogleSSO(client_id="your-google-client-id", client_secret="your-google-client-secret", redirect_uri="your-redirect-uri")

@router.get("/login/google")
async def google_login(request: Request):
    return await google_sso.get_login_redirect()

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    user = await google_sso.verify_and_process(request)
    if user:
        # Handle the authenticated user
        return {"email": user.email, "name": user.display_name}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google authentication failed")