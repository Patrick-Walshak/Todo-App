from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.db import get_db
from app.todos.schemas import (
    TodoCreateRequest,
    TodoDeleteResponse,
    TodoListResponse,
    TodoResponse,
    TodoUpdateRequest,
)
from app.todos.service import create_todo, delete_todo, get_user_todos, update_todo

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create(
    payload: TodoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo(db, current_user.id, payload)


@router.get("", response_model=TodoListResponse, status_code=status.HTTP_200_OK)
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todos = get_user_todos(db, current_user.id)
    return TodoListResponse(todos=todos, count=len(todos))


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update(
    todo_id: int,
    payload: TodoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_todo(db, todo_id, current_user.id, payload)


@router.delete("/{todo_id}", response_model=TodoDeleteResponse, status_code=status.HTTP_200_OK)
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_todo(db, todo_id, current_user.id)
    return TodoDeleteResponse(message="Todo deleted successfully.")
