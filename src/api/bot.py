from typing import Any

from fastapi import APIRouter, Request
import json

from src.slackbot import send


router = APIRouter()


@router.post("/subscribe")
async def send_msg(request: Request) -> Any:
    body = await request.body()
    data = json.loads(body)
    if 'event' in data:
        event = data['event']
        if event['type'] == 'app_mention':
            send.send_select_instance()


@router.post("/post")
def post() -> Any:
    body = await request.body()
    print(body)
    return None
