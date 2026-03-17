from data_models.post_image_data_model import PostImage
from models.post_image_model import PostImageModel


class PostImageMapper:
    @staticmethod
    def to_model(post_image: PostImage) -> PostImageModel:
        result = PostImageModel(
            id=post_image.id,
            post_id=post_image.post_id,
            image_url=post_image.image_url,
            order_index=post_image.order_index
        )

        return result

    @staticmethod
    def to_list_model(post_images: list[PostImage]) -> list[PostImageModel]:
        result = [PostImageMapper.to_model(post_image) for post_image in post_images]

        return result
