from sqlalchemy.orm import Session
from data_models.post_likes_data_model import PostLike

class PostLikeRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_like(self, user_id: int, post_id: int) -> PostLike | None:
        like = self.db_session.query(PostLike).filter_by(user_id=user_id, post_id=post_id).first()

        return like

    def create_like(self, user_id: int, post_id: int) -> PostLike:
        like = PostLike(user_id=user_id, post_id=post_id)
        self.db_session.add(like)
        self.db_session.commit()

        return like

    def delete_like(self, like: PostLike) -> PostLike:
        self.db_session.delete(like)
        self.db_session.commit()

        return like