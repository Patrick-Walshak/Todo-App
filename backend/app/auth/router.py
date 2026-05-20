from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterResponse, TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.auth.service import login_user, register_user
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload)
    return RegisterResponse(
        message="Account created successfully.",
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, payload)
    return TokenResponse(access_token=token)
