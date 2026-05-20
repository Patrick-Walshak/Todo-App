from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserLoginRequest, UserRegisterRequest
from app.core.exceptions import bad_request_exception, conflict_exception, credentials_exception
from app.core.security import create_access_token, hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def register_user(db: Session, payload: UserRegisterRequest) -> User:
    if get_user_by_email(db, payload.email):
        raise conflict_exception("An account with this email already exists.")

    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: UserLoginRequest) -> str:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password):
        raise credentials_exception()

    return create_access_token(subject=str(user.id))
