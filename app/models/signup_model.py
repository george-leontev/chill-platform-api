from pydantic import EmailStr
from models.app_base_model import AppBaseModel


class SignUpModel(AppBaseModel):
    user_name: str

    first_name: str

    last_name: str

    age: int

    email: EmailStr

    password: str

    confirmed_password: str