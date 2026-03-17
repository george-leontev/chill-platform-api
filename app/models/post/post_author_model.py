from models.app_base_model import AppBaseModel


class PostAuthorModel(AppBaseModel):
    id: int

    username: str

    first_name: str

    last_name: str

    age: int

    email: str
