from models.user_info_model import UserInfoModel
from data_models.post_data_model import Post
from data_models.post_likes_data_model import PostLike
from models.post.post_model import PostModel, PostsModel
from models.post_like_model import PostLikeModel
from models.post.post_like_info_model import PostLikeInfoModel
from mappers.post_image_mapper import PostImageMapper


class PostMapper:
    @staticmethod
    def to_model(post: Post, current_user_id: int = None) -> PostModel:
        is_liked = False
        if current_user_id is not None and hasattr(post, 'likes'):
            is_liked = any(like.user_id == current_user_id for like in post.likes)

        likes_info = []
        if hasattr(post, 'likes') and post.likes:
            likes_info = [
                PostLikeInfoModel(
                    user_id=like.user_id,
                    created_at=like.created_at
                )
                for like in post.likes
            ]

        result = PostModel(
            id=post.id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            author=UserInfoModel(
                id=post.user.id,
                first_name= post.user.first_name,
                last_name= post.user.last_name,
                username=post.user.username,
                email=post.user.email
            ),
            images=PostImageMapper.to_list_model(post.images) if post.images else [],
            is_liked=is_liked,
            likes=likes_info,
            likes_count=len(likes_info)
        )

        return result

    @staticmethod
    def to_list_model(posts: list[Post], total: int, page: int, size: int, current_user_id: int = None) -> PostsModel:
        pages = (total + size - 1) // size
        result = PostsModel(
            items=[PostMapper.to_model(post, current_user_id) for post in posts],
            total=total,
            page=page,
            size=size,
            pages=pages
        )

        return result

    @staticmethod
    def to_like_model(like: PostLike, liked: bool, like_count: int) -> PostLikeModel:
        result = PostLikeModel(
            user_id=like.user_id,
            post_id=like.post_id,
            liked=liked,
            like_count=like_count
        )

        return result