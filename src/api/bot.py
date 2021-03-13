from typing import Any

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json

from src.slackbot import send


router = APIRouter()


@router.post("/subscribe")
async def send_msg(request: Request) -> Any:
    body = await request.body()
    print(body)
    data = json.loads(body)

    data_type = data['type']
    if data_type == 'url_verification':
        resp = { 'challenge': data['challenge'] }
        return JSONResponse(content=jsonable_encoder(resp))

    print(data)
    if 'event' in data:
        event = data['event']
        if event['type'] == 'app_mention':
            if 'list' in event['text']:
                pass
            #  send.send_select_instance()


@router.post("/post")
async def post(payload: str = Form(...)) -> Any:
    data = json.loads(payload)
    print(json.dumps(data))

    if(data['callback_id'] == 'instance'):
        if (data['actions'][0]['name'] == 'cancel'):
            resp = {
                "delete_original": "true"
            }
            return JSONResponse(content=jsonable_encoder(resp))
        if (data['actions'][0]['name'] == 'selected'):
            instance_type = data['actions'][0]['selected_options'][0]['value']
            print(instance_type)

        raise HTTPException(status_code=404, detail="Item not found")
