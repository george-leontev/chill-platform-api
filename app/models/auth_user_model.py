from models.app_base_model import AppBaseModel


class AuthUserModel(AppBaseModel):
    token: str

    email: str

    user_id: int

    role_id: int
