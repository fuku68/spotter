from typing import Any

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import re
import json

from src.slackbot import sender
from src.aws import ec2


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

    if 'event' in data:
        event = data['event']
        if event['type'] == 'app_mention':
            if 'list' in event['text']:
                sender.send_instance_list()
            elif 'deploy' in event['text']:
                sender.send_select_instance()
            elif 'drop' in event['text']:
                r = re.search(r'drop\s+(\S+)', event['text'].strip())
                if r and r.group(1):
                    sender.send_drop_instance(r.group(1))


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
            user = data['user']['name']
            instance_type = data['actions'][0]['selected_options'][0]['value']
            try:
                instance = ec2.create_spot_instance(instance_type=instance_type, user=user)
                attachment = sender.create_spot_instance_attachment(instance)
                resp = {
                    "replace_original": "true",
                    "attachments": [attachment],
                }
                return JSONResponse(content=jsonable_encoder(resp))

            except Exception as e:
                resp = {
                    "replace_original": "true",
                    "text": "ERROR: " + e,
                }
                return JSONResponse(content=jsonable_encoder(resp))

    raise HTTPException(status_code=404, detail="Item not found")
