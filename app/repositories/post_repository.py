from sqlalchemy.orm import Session
from data_models.post_data_model import Post

class PostRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> list[Post]:
        posts = self.db_session.query(Post).all()

        return posts

    def get_by_id(self, post_id: int) -> Post | None:
        post = self.db_session.query(Post).filter(Post.id == post_id).one_or_none()

        return post

    def get_by_user_id(self, user_id: int) -> list[Post]:
        post = self.db_session.query(Post).filter(Post.user_id == user_id).all()

        return post

    def create(self, title: str, content: str, user_id: int) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        self.db_session.add(post)
        self.db_session.commit()

        return post

    def update(self, post: Post, title: str, content: str) -> Post:
        post.title = title
        post.content = content
        self.db_session.commit()

        return post

    def delete(self, post: Post) -> Post:
        self.db_session.delete(post)
        self.db_session.commit()

        return post
