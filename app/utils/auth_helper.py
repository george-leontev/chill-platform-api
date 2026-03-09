from sqlalchemy.orm import Session
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
import jwt
import os
from models.enums.user_role_enum import UserRoleEnum
from database import get_db
from data_models.user_data_model import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def verify_token(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Токен не найден.")

    token = auth_header.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("email"):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Токен не содержит email.")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Срок токена истёк.")
    except jwt.JWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Неверный токен.")

def verify_token_from_string(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload.get("email"):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Токен не содержит email.')

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Срок токена истёк.')

    except jwt.JWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Неверный токен.')

def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == payload["email"]).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Пользователь не найден.")

    return user

def authorize(roles: list[UserRoleEnum]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if UserRoleEnum(current_user.role_id) not in roles:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Недостаточно прав.")

        return current_user

    return role_checker
