

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dotenv import load_dotenv
from datetime import timedelta

from ..users.functions import get_all_user_data_by_email_or_name
from .encryption import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password

load_dotenv()

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/login",
             tags=['authentication'],
             description="Log in the user and get the token.")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    user = authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(email: str, password: str):
    user = get_all_user_data_by_email_or_name(email=email)

    if not user:
        return False

    if not verify_password(password, user['password']):
        return False

    return user



