from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.models import User
from app.core.exceptions import credentials_exception
from app.core.security import decode_access_token
from app.db import get_db

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    user_id = decode_access_token(token)

    if user_id is None:
        raise credentials_exception()

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception()

    return user
