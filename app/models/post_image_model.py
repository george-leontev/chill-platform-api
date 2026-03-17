from models.app_base_model import AppBaseModel


class PostImageModel(AppBaseModel):
    id: int

    post_id: int

    image_url: str

    order_index: int
