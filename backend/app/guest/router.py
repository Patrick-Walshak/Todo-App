from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.guest.schemas import GuestTodoCreateRequest, GuestTodoListResponse, GuestTodoResponse
from app.guest.service import create_guest_todo, get_all_guest_todos

router = APIRouter(prefix="/guest/todos", tags=["Guest Todos"])


@router.post("", response_model=GuestTodoResponse, status_code=status.HTTP_201_CREATED)
def create(payload: GuestTodoCreateRequest, db: Session = Depends(get_db)):
    return create_guest_todo(db, payload)


@router.get("", response_model=GuestTodoListResponse, status_code=status.HTTP_200_OK)
def list_todos(db: Session = Depends(get_db)):
    todos = get_all_guest_todos(db)
    return GuestTodoListResponse(todos=todos, count=len(todos))
