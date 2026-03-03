from models.app_base_model import AppBaseModel


class AuthUserModel(AppBaseModel):
    email: str

    user_id: int

    role_id: int

    token: str
