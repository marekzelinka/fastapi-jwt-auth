from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str
