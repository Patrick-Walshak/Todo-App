from datetime import datetime

from pydantic import BaseModel, field_validator

from app.todos.models import TodoStatus


class TodoCreateRequest(BaseModel):
    title: str
    body: str

    @field_validator("title", "body")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be blank.")
        return value.strip()


class TodoUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    status: TodoStatus | None = None

    @field_validator("title", "body", mode="before")
    @classmethod
    def not_blank(cls, value: str | None) -> str | None:
        if value is not None and not str(value).strip():
            raise ValueError("This field must not be blank.")
        return value.strip() if value else value


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    count: int


class TodoDeleteResponse(BaseModel):
    message: str
