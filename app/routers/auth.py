from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from app.core.auth import (
    create_access_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.db.schema import Token, User, UserCreate, UserPublic
from app.db.session import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
async def register_user(*, session: SessionDep, user: Annotated[UserCreate, Body()]):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    print(f"{user.password=}")
    hashed_password = hash_password(user.password)
    new_user = User(**user.model_dump(), hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    *, session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> User:
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
