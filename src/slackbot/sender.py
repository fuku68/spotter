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
    instances = ec2.list()

    attachments = []
    for spot_request in requests:
        instance = next(filter(lambda x: x['InstanceId'] == spot_request['InstanceId'], instances), None)
        attachment = create_spot_instance_attachment(spot_request, instance)
        attachments.append(attachment)

    response = client.chat_postMessage(
       channel='#sandbox',
       text="INSTANCE LIST",
       attachments=attachments)


def create_spot_instance_attachment(spot, instance = {}):
  specification = spot['LaunchSpecification'] if 'LaunchSpecification' in spot.keys() else {}
  tags = spot['Tags']
  created_by = ''
  for tag in tags:
      if tag['Key'] == 'created_by':
          created_by = tag['Value']

  attachment = {
      'title': spot['InstanceId'],
      'color': 'good' if spot['State'] == 'active' else '#FF0000',
      "fields": [{
          "title": "InstanceType",
          "value": specification['InstanceType']  if 'InstanceType' in specification.keys() else '',
          "short": "true"
      }, {
          "title": "SpotPrice",
          "value": spot['SpotPrice'],
          "short": "true"
      }, {
          "title": "State",
          "value": spot['State'],
          "short": "true"
      }, {
          "title": "IP",
          "value": instance['PublicIpAddress'] if 'PublicIpAddress' in instance.keys() else '',
          "short": "true"
      }, {
          "title": "CreatedAt",
          "value": spot['CreateTime'].strftime("%Y/%m/%d %H:%M"),
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
    response = client.chat_postMessage(
       channel='#sandbox',
       text="DEPLOY INSTANCE!",
       attachments=attachments)


def send_drop_instance(instance_id):
    drop_id = ec2.terminate_instance(instance_id)

    client = WebClient(settings.SLACK_TOKEN)
    response = client.chat_postMessage(
       channel='#sandbox',
       text="DROP INSTANCE: " + drop_id)
