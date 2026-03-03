from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.enums.user_role_enum import UserRoleEnum
from utils.auth_helper import authorize
from models.post.update_post_model import CreateOrUpdatePostModel
from models.post.post_model import PostModel, PostsModel
from data_models.post_data_model import Post
from data_models.user_data_model import User
from database import get_db


router = APIRouter()

@router.get('/posts', tags=['Posts'], response_model=PostsModel)
async def get_all_posts(
    current_user: User = Depends(
        authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])
    ),
    db_session: Session = Depends(get_db),
):
    print(current_user.id)
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

@router.get('/posts/{id}', tags=['Posts'], response_model=PostModel)
async def get_post_by_id(post_id: int, db_session: Session = Depends(get_db)):
    post = db_session. \
        query(Post). \
        filter(Post.id == post_id). \
        one_or_none() \

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.',
        )

    return PostModel(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

@router.post('/posts', tags=['Posts'], response_model=PostModel)
async def create_post(body: CreateOrUpdatePostModel, db_session: Session = Depends(get_db)):
    new_post = Post(
        title=body.title,
        content=body.content,
        user_id=1
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

@router.put('/posts/{id}', tags=['Posts'], response_model=PostModel)
async def edit_post(post_id: int, body: CreateOrUpdatePostModel, db_session: Session = Depends(get_db)):
    edited_post = db_session \
        .query(Post) \
        .filter(Post.id == post_id) \
        .one_or_none()

    if not edited_post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.'
        )

    # if post.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=HTTPStatus.FORBIDDEN,
    #         detail='Недостаточно прав для редактирования этой публикации.'
    #     )

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

@router.delete('/posts/{id}', tags=['Posts'], response_model=PostModel)
async def delete_post(id: int, db_session: Session = Depends(get_db)):
    post = db_session. \
        query(Post). \
        filter(Post.id == id). \
        one_or_none() \

    if not post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Публикация не найдена.',
        )

    db_session.delete(post)
    db_session.commit()

    result = PostModel(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    return result
