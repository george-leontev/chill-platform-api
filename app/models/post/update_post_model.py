from typing import Optional, List
from models.app_base_model import AppBaseModel


class CreateOrUpdatePostModel(AppBaseModel):
    title: str

    content: str

    images: Optional[List[str]] = []
