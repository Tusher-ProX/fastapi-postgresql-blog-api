from fastapi import APIRouter
from .endpoints.posts import router as post_router
from .endpoints.users import router as user_router
from .endpoints.auth import router as auth_router
from .endpoints.votes import router as vote_router

api_router = APIRouter()

api_router.include_router(post_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(vote_router)