import os
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ...authentication.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from ...schemas.user_schema import UserSchema, UserCreate
from ...models.user_model import User
from ...db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import Response
from fastapi import APIRouter
from ...config import settings


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication routes"])


@router.post("/register", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
