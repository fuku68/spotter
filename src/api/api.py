from fastapi import APIRouter

from src.api import bot

api_router = APIRouter()

@api_router.get("")
def read_root():
    return {"Hello": "World"}

api_router.include_router(bot.router, tags=["bot"])
