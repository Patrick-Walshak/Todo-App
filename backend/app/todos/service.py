from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import forbidden_exception, not_found_exception
from app.todos.models import Todo
from app.todos.schemas import TodoCreateRequest, TodoUpdateRequest


def create_todo(db: Session, user_id: int, payload: TodoCreateRequest) -> Todo:
    todo = Todo(user_id=user_id, title=payload.title, body=payload.body)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_user_todos(db: Session, user_id: int) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).all()


def _get_todo_or_404(db: Session, todo_id: int) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise not_found_exception("Todo")
    return todo


def _assert_owner(todo: Todo, user_id: int) -> None:
    if todo.user_id != user_id:
        raise forbidden_exception()


def update_todo(db: Session, todo_id: int, user_id: int, payload: TodoUpdateRequest) -> Todo:
    todo = _get_todo_or_404(db, todo_id)
    _assert_owner(todo, user_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int, user_id: int) -> None:
    todo = _get_todo_or_404(db, todo_id)
    _assert_owner(todo, user_id)
    db.delete(todo)
    db.commit()
