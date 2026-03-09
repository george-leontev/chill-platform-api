from data_models.post_data_model import Post
from data_models.post_likes_data_model import PostLike
from models.post.post_model import PostModel, PostsModel
from models.post_like_model import PostLikeModel


class PostMapper:
    @staticmethod
    def to_model(post: Post) -> PostModel:
        result = PostModel(
            id=post.id,
            title=post.title,
            content=post.content,
            user_id=post.user_id
        )

        return result

    @staticmethod
    def to_list_model(posts: list[Post]) -> PostsModel:
        result = PostsModel(
            items=[PostMapper.to_model(post) for post in posts]
        )

        return result

    @staticmethod
    def to_like_model(like: PostLike, liked: bool) -> PostLikeModel:
        result = PostLikeModel(
            user_id=like.user_id,
            post_id=like.post_id,
            liked=liked
        )

        return result