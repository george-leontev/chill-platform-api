from models.app_base_model import AppBaseModel


class UserInfoModel(AppBaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
