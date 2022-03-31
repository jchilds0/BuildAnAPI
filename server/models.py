from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    email: str
    age: int = Field(..., gt=0)
    password: str
    notes: list[str]


class UpdateUser(BaseModel):
    username: str | None
    email: str | None
    age: int | None
    password: str | None
    notes: list[str] | None
