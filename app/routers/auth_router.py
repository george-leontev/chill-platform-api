from datetime import datetime, timedelta, timezone
from hashlib import sha256
from http import HTTPStatus
import os
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import jwt
from database import get_db
from data_models.user_data_model import User
from models.auth_user_model import AuthUserModel
from models.signin_model import SignInModel


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/sign-in", response_model=AuthUserModel)
def signin(body: SignInModel, db: Session = Depends(get_db)):
    account: User = db.query(User).where(body.email == User.email).first()

    if not account:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Не удалось войти в систему. Пользователь не найден.'
        )

    hashed_signin_password = sha256(body.password.encode(encoding="utf-8")).hexdigest()

    if hashed_signin_password == account.password:
        expiration = datetime.now(timezone.utc) + timedelta(days=1)
        token_payload = {
            "email": account.email,
            "exp": expiration,
            "user_id": account.id,
            "role": account.role_id
        }

        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

        return AuthUserModel(
            email=account.email,
            user_id=account.id,
            role_id=account.role_id,
            token=token
        )
