from fastapi import APIRouter
from routers import auth_router, post_router

router = APIRouter(prefix="/api")

router.include_router(auth_router.router, tags=["Authentication"])
router.include_router(post_router.router, tags=["Posts"])