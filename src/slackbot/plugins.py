import json
from slackbot.bot import respond_to

from src.aws import ec2

@respond_to('list')
def list(message):
    # Slackに応答を返す
    message.reply('こんにちは!')
    ec2.list()


@respond_to('deploy')
def deploy(message):
    print(message.user)
    attachments_json = [{
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#258ab5",
        "attachment_type": "default",
        "callback_id": "the_greatest_war",
        "actions": [{
            "name": "instance_type",
            "text": "instance type",
            "type": "select",
            "options": [
                {
                    "text": "Hearts",
                    "value": "hearts"
                },
                {
                    "text": "Bridge",
                    "value": "bridge"
                },
            ]
        }, {
            "name": "cancel",
            "type": "button",
            "text": {
                "type": "cancel",
                "text": "Cancel"
            },
            "value": "cancel",
            "action_id": "button_1",
        }]
    }]

    message.send_webapi('', json.dumps(attachments_json))


@respond_to('instance_type')
def deploy(message):
    print('instance_type')
