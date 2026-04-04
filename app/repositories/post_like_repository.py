from sqlalchemy.orm import Session, joinedload
from data_models.post_likes_data_model import PostLike
from data_models.post_data_model import Post

class PostLikeRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_like(self, user_id: int, post_id: int) -> PostLike | None:
        like = self.db_session.query(PostLike).filter_by(user_id=user_id, post_id=post_id).first()

        return like

    def create_like(self, user_id: int, post_id: int) -> tuple[PostLike, int]:
        like = PostLike(user_id=user_id, post_id=post_id)
        self.db_session.add(like)
        self.db_session.commit()

        like_count = self.db_session.query(PostLike).filter_by(post_id=post_id).count()

        return like, like_count

    def delete_like(self, like: PostLike) -> tuple[PostLike, int]:
        post_id = like.post_id
        self.db_session.delete(like)
        self.db_session.commit()

        like_count = self.db_session.query(PostLike).filter_by(post_id=post_id).count()

        return like, like_count

    def get_liked_posts(self, user_id: int, page: int, size: int) -> tuple[list[Post], int]:
        query = self.db_session.query(Post).\
            join(PostLike).\
            filter(PostLike.user_id == user_id).\
            options(joinedload(Post.user), joinedload(Post.images), joinedload(Post.likes))

        total = query.count()
        posts = query.order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return posts, total