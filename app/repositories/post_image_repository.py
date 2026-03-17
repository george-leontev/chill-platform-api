from sqlalchemy.orm import Session
from data_models.post_image_data_model import PostImage


class PostImageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, post_id: int, image_url: str, order_index: int = 0) -> PostImage:
        post_image = PostImage(post_id=post_id, image_url=image_url, order_index=order_index)
        self.db_session.add(post_image)
        self.db_session.commit()

        return post_image

    def create_many(self, post_id: int, image_urls: list[str]) -> list[PostImage]:
        post_images = [
            PostImage(post_id=post_id, image_url=url, order_index=i)
            for i, url in enumerate(image_urls)
        ]
        self.db_session.add_all(post_images)
        self.db_session.commit()

        return post_images

    def delete_by_post_id(self, post_id: int) -> None:
        self.db_session.query(PostImage).filter(PostImage.post_id == post_id).delete()
        self.db_session.commit()
