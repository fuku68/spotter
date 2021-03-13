from src.core.config import settings

from slack import WebClient

from .instances import instances

def send_select_instance() -> None:
    client = WebClient(settings.SLACK_TOKEN)
    print(settings.SLACK_TOKEN)
    # channels = client.api_call("channels.list")

    instance_options = ({ "text": x, "value": x} for x in instances)

    attachments = [
        {
            "text": "Choose a instance type",
            "fallback": "You are unable to choose a game",
            "callback_id": "instance",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                 {
                    "name": "games_list",
                    "text": "Pick a game...",
                    "type": "select",
                    "options": list(instance_options),
                },
                {
                    "name": "ok",
                    "text": "OK",
                    "type": "button",
                    "value": "ok"
                },
                {
                    "name": "cancel",
                    "text": "CANCEL",
                    "type": "button",
                    "value": "cancel"
                }
            ]
        }
    ]

    esponse = client.chat_postMessage(
       channel='#sandbox',
       text="Hello world!",
       attachments=attachments)
