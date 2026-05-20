from datetime import datetime

from pydantic import BaseModel, field_validator


class GuestTodoCreateRequest(BaseModel):
    title: str
    body: str

    @field_validator("title", "body")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be blank.")
        return value.strip()


class GuestTodoResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}


class GuestTodoListResponse(BaseModel):
    todos: list[GuestTodoResponse]
    count: int
