"""seed_initial_data

Revision ID: c7cb0244a8b6
Revises: 80f982c8024d
Create Date: 2026-03-02 15:10:28.320856

"""
from datetime import datetime
from hashlib import sha256
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.enums.friend_status_enum import FriendStatusEnum
from models.enums.user_role_enum import UserRoleEnum


# revision identifiers, used by Alembic.
revision: str = 'c7cb0244a8b6'
down_revision: Union[str, Sequence[str], None] = '80f982c8024d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

password = '123456789'
hashed_password = sha256(password.encode(encoding="utf-8")).hexdigest()

def upgrade():
    # Seed user roles
    roles_table = sa.table('user_role',
        sa.column('id', sa.Integer),
        sa.column('role', sa.String),
    )

    op.bulk_insert(roles_table, [
        {'id': UserRoleEnum.MODERATOR, 'role': 'MODERATOR'},
        {'id': UserRoleEnum.USER, 'role': 'USER'},
    ])

    # Seed friend statuses
    status_table = sa.table('friend_status',
        sa.column('id', sa.Integer),
        sa.column('status', sa.String),
    )

    op.bulk_insert(status_table, [
        {'id': FriendStatusEnum.PENDING, 'status': 'pending'},
        {'id': FriendStatusEnum.ACCEPTED, 'status': 'accepted'},
    ])

    # Seed test users (with password hashed - use bcrypt)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    users_table = sa.table('users',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String),
        sa.column('username', sa.String),
        sa.column('password', sa.String),
        sa.column('role_id', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )

    op.bulk_insert(users_table, [
        {
            'id': 1,
            'email': 'MODERATOR@example.com',
            'username': 'MODERATOR',
            'password': hashed_password,
            'role_id': UserRoleEnum.MODERATOR,
        },
        {
            'id': 2,
            'email': 'john@example.com',
            'username': 'john_doe',
            'password': hashed_password,
            'role_id': UserRoleEnum.USER,
        },
        {
            'id': 3,
            'email': 'jane@example.com',
            'username': 'jane_smith',
            'password':hashed_password,
            'role_id': UserRoleEnum.USER,
        },
    ])

    # Seed posts
    posts_table = sa.table('posts',
        sa.column('id', sa.Integer),
        sa.column('title', sa.String),
        sa.column('content', sa.String),
        sa.column('user_id', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )

    op.bulk_insert(posts_table, [
        {
            'id': 1,
            'title': 'Welcome Post',
            'content': 'Welcome to our platform! This is the first post.',
            'user_id': 1,

        },
        {
            'id': 2,
            'title': 'Hello World',
            'content': 'This is my first post on this amazing platform!',
            'user_id': 2,

        },
        {
            'id': 3,
            'title': 'Tips and Tricks',
            'content': 'Here are some tips and tricks for using this app...',
            'user_id': 3,

        },
    ])

    # Seed messages
    messages_table = sa.table('messages',
        sa.column('id', sa.Integer),
        sa.column('content', sa.String),
        sa.column('sender_id', sa.Integer),
        sa.column('receiver_id', sa.Integer),
        sa.column('is_read', sa.Boolean),
        sa.column('created_at', sa.DateTime)
    )

    op.bulk_insert(messages_table, [
        {
            'id': 1,
            'content': 'Hey John, how are you?',
            'sender_id': 3,
            'receiver_id': 2,
            'is_read': False,

        },
        {
            'id': 2,
            'content': 'Hi Jane, I am doing great!',
            'sender_id': 2,
            'receiver_id': 3,
            'is_read': False,

        },
    ])

    # Seed friends
    friends_table = sa.table('friends',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('friend_id', sa.Integer),
        sa.column('status_id', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )

    op.bulk_insert(friends_table, [
        {
            'id': 1,
            'user_id': 2,
            'friend_id': 3,
            'status_id': FriendStatusEnum.ACCEPTED,

        },
        {
            'id': 2,
            'user_id': 3,
            'friend_id': 2,
            'status_id': FriendStatusEnum.ACCEPTED,

        },
    ])

def downgrade():
    # Remove seeded data in reverse order (respect foreign key constraints)
    op.execute("DELETE FROM friends WHERE id IN (1, 2)")
    op.execute("DELETE FROM messages WHERE id IN (1, 2)")
    op.execute("DELETE FROM posts WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM users WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM user_role WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM friend_status WHERE id IN (1, 2, 3, 4)")