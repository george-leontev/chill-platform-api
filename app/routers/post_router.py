from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.enums.user_role_enum import UserRoleEnum
from utils.auth_helper import authorize
from models.post.update_post_model import CreateOrUpdatePostModel
from models.post.post_model import PostModel, PostsModel
from models.post_like_model import PostLikeModel
from data_models.user_data_model import User
from repositories.post_repository import PostRepository
from repositories.post_like_repository import PostLikeRepository
from services.post_service import PostService

router = APIRouter()

def get_post_service(db_session: Session = Depends(get_db)) -> PostService:
    return PostService(
        post_repository=PostRepository(db_session),
        like_repository=PostLikeRepository(db_session)
    )

@router.get('/posts', tags=['Posts'], response_model=PostsModel, dependencies=[Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER]))])
async def get_all_posts(post_service: PostService = Depends(get_post_service)):
    posts = post_service.get_all()
    result = PostsModel(
        items=[
            PostModel(
                id=p.id,
                content=p.content,
                title=p.title,
                user_id=p.user_id
            ) for p in posts
        ]
    )

    return result

@router.get('/posts/my', tags=['Posts'], response_model=PostsModel)
async def get_my_posts(
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        post_service: PostService = Depends(get_post_service)
    ):
    posts = post_service.get_my_posts(current_user.id)
    result = PostsModel(
        items=[
            PostModel(
                id=p.id,
                content=p.content,
                title=p.title,
                user_id=p.user_id
            ) for p in posts
        ]
    )

    return result

@router.get('/posts/{post_id}', tags=['Posts'], response_model=PostModel, dependencies=[Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER]))])
async def get_post_by_id(post_id: int, post_service: PostService = Depends(get_post_service)):
    post = post_service.get_by_id(post_id)
    result = PostModel(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    return result

@router.post('/posts', tags=['Posts'], response_model=PostModel)
async def create_post(
        body: CreateOrUpdatePostModel,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        post_service: PostService = Depends(get_post_service)
    ):
    post = post_service.create(title=body.title, content=body.content, current_user=current_user)
    result = PostModel(
        id=post.id,
        content=post.content,
        title=post.title,
        user_id=post.user_id
    )

    return result

@router.put('/posts/{post_id}', tags=['Posts'], response_model=PostModel)
async def edit_post(
        post_id: int,
        body: CreateOrUpdatePostModel,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        post_service: PostService = Depends(get_post_service)
    ):
    post = post_service.update(post_id=post_id, title=body.title, content=body.content, current_user=current_user)
    return PostModel(id=post.id, content=post.content, title=post.title, user_id=post.user_id)

@router.delete('/posts/{post_id}', tags=['Posts'], response_model=PostModel)
async def delete_post(
        post_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        post_service: PostService = Depends(get_post_service)
    ):
    post = post_service.delete(post_id=post_id, current_user=current_user)
    result = PostModel(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    return result

@router.post('/posts/{post_id}/like', response_model=PostLikeModel)
async def toggle_like(
        post_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        post_service: PostService = Depends(get_post_service)
    ):
    result = post_service.toggle_like(post_id=post_id, current_user=current_user)

    return result
