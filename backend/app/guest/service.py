from sqlalchemy.orm import Session

from app.guest.models import GuestTodo
from app.guest.schemas import GuestTodoCreateRequest


def create_guest_todo(db: Session, payload: GuestTodoCreateRequest) -> GuestTodo:
    todo = GuestTodo(title=payload.title, body=payload.body)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_all_guest_todos(db: Session) -> list[GuestTodo]:
    return db.query(GuestTodo).order_by(GuestTodo.created_at.desc()).all()
