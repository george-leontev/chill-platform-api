from models.app_base_model import AppBaseModel


class CreateOrUpdatePostModel(AppBaseModel):
    title: str

    content: str
