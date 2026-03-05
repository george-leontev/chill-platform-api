from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from database import get_db
from sqlalchemy.orm import Session
from utils.auth_helper import authorize
from models.enums.user_role_enum import UserRoleEnum
from models.post_like_model import PostLikeModel
from models.post.update_post_model import CreateOrUpdatePostModel
from models.post.post_model import PostModel, PostsModel
from data_models.post_likes_data_model import PostLike
from data_models.post_data_model import Post
from data_models.user_data_model import User


router = APIRouter()

@router.get('/posts', tags=['Posts'], response_model=PostsModel, dependencies=[Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER]))])
async def get_all_posts(db_session: Session = Depends(get_db)):
    posts = db_session.query(Post).all()

    data = PostsModel(
        items=[
            PostModel(
                id=post.id,
                content=post.content,
                title=post.title,
                user_id=post.user_id
            )
            for post in posts
        ]
    )

    return data

@router.get('/posts/my', tags=['Posts'], response_model=PostsModel)
async def get_my_posts(
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        db_session: Session = Depends(get_db)
    ):
    my_posts = db_session. \
        query(Post). \
        filter(Post.user_id == current_user.id). \
        all()

    result = PostsModel(items=[
        PostModel(
            id=post.id,
            content=post.content,
            title=post.title,
            user_id=post.user_id
        ) for post in my_posts]
    )

    return result

@router.get('/posts/{post_id}', tags=['Posts'], response_model=PostModel, dependencies=[Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER]))])
async def get_post_by_id(post_id: int, db_session: Session = Depends(get_db)):
    post = db_session. \
        query(Post). \
        filter(Post.id == post_id). \
        one_or_none()

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.',
        )

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
        db_session: Session = Depends(get_db)
    ):
    new_post = Post(
        title=body.title,
        content=body.content,
        user_id=current_user.id
    )
    db_session.add(new_post)
    db_session.commit()

    result = PostModel(
        id=new_post.id,
        content=new_post.content,
        title=new_post.title,
        user_id=new_post.user_id
    )

    return result

@router.put('/posts/{post_id}', tags=['Posts'], response_model=PostModel)
async def edit_post(
        post_id: int,
        body: CreateOrUpdatePostModel,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        db_session: Session = Depends(get_db)
    ):
    edited_post = db_session \
        .query(Post) \
        .filter(Post.id == post_id) \
        .one_or_none()

    if not edited_post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.'
        )

    if edited_post.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Недостаточно прав для редактирования этой публикации.'
        )

    edited_post.content = body.content
    edited_post.title = body.title
    db_session.commit()

    result = PostModel(
        id=edited_post.id,
        content=edited_post.content,
        title=edited_post.title,
        user_id=edited_post.user_id
    )

    return result

@router.delete('/posts/{post_id}', tags=['Posts'], response_model=PostModel)
async def delete_post(
        post_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
        db_session: Session = Depends(get_db)
    ):
    deleted_post = db_session. \
        query(Post). \
        filter(Post.id == post_id). \
        one_or_none()

    if not deleted_post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.',
        )

    if deleted_post.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Недостаточно прав для удаления этой публикации.'
        )

    db_session.delete(deleted_post)
    db_session.commit()

    result = PostModel(
        id=deleted_post.id,
        title=deleted_post.title,
        content=deleted_post.content,
        user_id=deleted_post.user_id
    )

    return result

@router.post('/posts/{post_id}/like')
async def toggle_like(
    post_id: int,
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    db_session: Session = Depends(get_db)
):
    post = db_session.query(Post).get(post_id)

    if not post:
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Публикация не найдена.',
            )

    existing = db_session. \
        query(PostLike). \
        filter_by(user_id=current_user.id, post_id=post_id). \
        first()

    if existing:
        db_session.delete(existing)
        db_session.commit()

        return PostLikeModel(
            user_id=current_user.id,
            post_id=post_id,
            liked=False
        )
    else:
        db_session.add(PostLike(user_id=current_user.id, post_id=post_id))
        db_session.commit()

        return PostLikeModel(
            user_id=current_user.id,
            post_id=post_id,
            liked=True
        )
