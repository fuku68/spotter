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
                    "name": "selected",
                    "text": "select instance type...",
                    "type": "select",
                    "options": list(instance_options),
                },
                {
                    "name": "cancel",
                    "style": "danger",
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
