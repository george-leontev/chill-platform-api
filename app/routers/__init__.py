from fastapi import APIRouter
from routers import auth_router, post_router, friend_router, message_router, profile_router

router = APIRouter(prefix="/api")

router.include_router(auth_router.router, tags=["Authentication"])
router.include_router(post_router.router, tags=["Posts"])
router.include_router(friend_router.router, tags=["Friends"])
router.include_router(message_router.router, tags=["Messaging"])
router.include_router(profile_router.router, tags=["Profiles"])