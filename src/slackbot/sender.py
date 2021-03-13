from slack import WebClient

from src.core.config import settings
from src.aws import ec2
from .instances import instances

import json

def send_error(err) -> None:
    pass


def send_instance_list() -> None:
    client = WebClient(settings.SLACK_TOKEN)
    requests = ec2.spot_request_list()

    attachments = []
    for instance in requests:
        print(instance)
        attachment = create_spot_instance_attachment(instance)
        attachments.append(attachment)

    response = client.chat_postMessage(
       channel='#sandbox',
       text="INSTANCE LIST",
       attachments=attachments)


def create_spot_instance_attachment(instance):
  specification = instance['LaunchSpecification']
  tags = instance['Tags']
  created_by = ''
  for tag in tags:
      if tag['Key'] == 'created_by':
          created_by = tag['Value']

  attachment = {
      'title': instance['InstanceId'],
      'color': 'good' if instance['State'] == 'active' else '#FF0000',
      "fields": [{
          "title": "InstanceType",
          "value": specification['InstanceType'],
          "short": "true"
      }, {
          "title": "SpotPrice",
          "value": instance['SpotPrice'],
          "short": "true"
      }, {
          "title": "State",
          "value": instance['State'],
          "short": "true"
      }, {
          "title": "CreatedAt",
          "value": instance['CreateTime'].strftime("%Y/%m/%d %H:%M"),
          "short": "true"
      }, {
          "title": "CreatedBy",
          "value": created_by,
          "short": "true"
      }]
  }
  return attachment


def send_select_instance() -> None:
    client = WebClient(settings.SLACK_TOKEN)

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
       text="DEPLOY INSTANCE!",
       attachments=attachments)