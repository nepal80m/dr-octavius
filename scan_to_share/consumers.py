import json
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.core.management.utils import get_random_secret_key
from scan_to_share.models import ScanRequest
from asgiref.sync import async_to_sync
import shortuuid


class ScanRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = shortuuid.uuid()
        self.session_secret = get_random_secret_key()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.send(
            text_data=json.dumps(
                {
                    "type": "websocket.accept",
                    "room": self.room_group_name,
                }
            )
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        message = text_data_json["message"]

        self.send(
            text_data=json.dumps(
                {"type": "message.receive", "message": "Message Received"}
            )
        )

    def request_approval(self, event):
        # message = event["message"]
        # status = event["status"]
        # approved_data = event["approved_data"]
        self.send(text_data=json.dumps(event))

    # def disconnect(self, code):
    #     return super().disconnect(code)
