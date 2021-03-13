from fastapi import APIRouter

from src.api import bot

api_router = APIRouter()

api_router.include_router(bot.router, prefix="/bot", tags=["bot"])
