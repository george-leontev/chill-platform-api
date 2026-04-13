from sqlalchemy.orm import Session, joinedload
from data_models.post_data_model import Post
from data_models.post_image_data_model import PostImage
from data_models.user_data_model import User
from data_models.profile_data_model import Profile

class PostRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_all(self, page: int, size: int) -> tuple[list[Post], int]:
        query = self.db_session.query(Post).options(
            joinedload(Post.user).joinedload(User.profile),
            joinedload(Post.images),
            joinedload(Post.likes)
        )
        total = query.count()
        posts = query.order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return posts, total

    def get_by_id(self, post_id: int) -> Post | None:
        post = self. \
                db_session. \
                query(Post). \
                options(
                    joinedload(Post.user).joinedload(User.profile),
                    joinedload(Post.images),
                    joinedload(Post.likes)
                ). \
                filter(Post.id == post_id). \
                one_or_none()

        return post

    def get_by_user_id(self, user_id: int, page: int, size: int) -> tuple[list[Post], int]:
        query = self.db_session.query(Post).options(
            joinedload(Post.user).joinedload(User.profile),
            joinedload(Post.images),
            joinedload(Post.likes)
        ).filter(Post.user_id == user_id)
        total = query.count()
        posts = query.order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return posts, total

    def create(self, title: str, content: str, user_id: int, image_urls: list[str] = None) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        self.db_session.add(post)
        self.db_session.flush()
        if image_urls:
            post_images = [
                PostImage(post_id=post.id, image_url=url, order_index=i)
                for i, url in enumerate(image_urls)
            ]
            self.db_session.add_all(post_images)
        self.db_session.commit()
        self.db_session.refresh(post)  # ← re-fetches created_at from DB with tz info
        return post

    def update(self, post: Post, title: str, content: str, image_urls: list[str] = None) -> Post:
        post.title = title
        post.content = content

        if image_urls is not None:
            # Delete existing images
            self.db_session.query(PostImage).filter(PostImage.post_id == post.id).delete()

            # Add new images
            post_images = [
                PostImage(post_id=post.id, image_url=url, order_index=i)
                for i, url in enumerate(image_urls)
            ]
            self.db_session.add_all(post_images)

        self.db_session.commit()

        return post

    def delete(self, post: Post) -> Post:
        self.db_session.delete(post)
        self.db_session.commit()

        return post
