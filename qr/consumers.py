import json
import shortuuid
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.core.management.utils import get_random_secret_key

from qr.models import IdentityAccessRequest, AuthorizedRequester, IdentityAccessPermit
from qr.serializers import IdentityAccessPermitSerializer
from history.models import ActivityHistory
from history.constants import QR_GENERATED, DOCUMENT_CODE_AGE, DOCUMENT_CODE_DVL


class IdentityAccessRequestConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_group_name = shortuuid.uuid()
        # self.session_secret = get_random_secret_key()
        # print(self.scope)
        headers = {x.decode(): y.decode() for x, y in self.scope["headers"]}
        print(headers)
        host = headers["host"]
        client = self.scope["client"]
        print(f"Got connection request from {host} OR,")
        print(f"Got connection request from {client[0]}")

        # Verify if the host is registered..
        requester = AuthorizedRequester.objects.filter(domain=host).first()

        # Override requester if it is localhost.
        if host.startswith("localhost"):
            requester, _ = AuthorizedRequester.objects.get_or_create(
                domain="http://localhost",
                defaults={
                    "name": "Local Host",
                    "requested_fields": ["NIN", "first_name", "caste"],
                },
            )

        if requester is None:
            print("Requester not verified. Connection rejected..")
            self.close()
            return

        view_request, _ = IdentityAccessRequest.objects.get_or_create(
            requester=requester, channel_name=self.channel_name
        )

        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )

        self.accept()
        self.send(
            text_data=json.dumps(
                {
                    "type": "request.registered",
                    "request_id": view_request.request_id,
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

    def access_request_approval(self, event):
        status = event["status"]
        data = event["data"]
        if status:

            self.send(
                text_data=json.dumps(
                    {
                        "type": "request.approved",
                        "message": "Your access request was approved.",
                        "data": data,
                    }
                )
            )
        else:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "request.rejected",
                        "message": "Your access request was rejected.",
                    }
                )
            )

    def disconnect(self, code):

        IdentityAccessRequest.objects.filter(channel_name=self.channel_name).delete()
        return super().disconnect(code)


class IdentityAccessPermitConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_group_name = shortuuid.uuid()
        # self.session_secret = get_random_secret_key()
        # print(self.scope)
        self.user = self.scope["user"]
        # print(self.scope)
        print(self.user)
        print(self.user.is_authenticated)
        if self.user.is_authenticated:
            print("Requester authenticated. Connection accepted..")
            self.accept()
        else:
            print("Requester not authenticated. Connection rejected..")
            self.close()

    def receive(self, text_data):
        print("Received message..")
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        if type == "permit.create":
            data = text_data_json["data"]
            print(f"Permit create request received with data {data}.")

            serializer = IdentityAccessPermitSerializer(data=data)
            if serializer.is_valid():
                access_permit = serializer.save(
                    permitted_by=self.user,
                    channel_name=self.channel_name,
                )
                print(
                    f"Created the access permit for user {self.user} with channel name {self.channel_name}"
                )

                permitted_document_code = access_permit.permitted_document_code
                if permitted_document_code == "AGE":
                    document = DOCUMENT_CODE_AGE
                elif permitted_document_code == "DVL":
                    document = DOCUMENT_CODE_DVL
                else:
                    document = ""
                ActivityHistory.objects.create(
                    user=self.user,
                    activity=QR_GENERATED.activity_code,
                    description=QR_GENERATED.description.format(document=document),
                )

                self.send(
                    text_data=json.dumps(
                        {
                            "type": "permit.create.success",
                            "message": "Access permit created.",
                            "data": {
                                "permit_id": access_permit.permit_id,
                                "permitted_document_code": access_permit.permitted_document_code,
                            },
                        }
                    )
                )
            else:
                print("Received invalid message")
                self.send(
                    text_data=json.dumps(
                        {
                            "type": "permit.create.error",
                            "message": "Error creating access permit.",
                            "data": serializer.errors,
                        }
                    )
                )

        else:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "message.unrecognized",
                        "message": "Message Received but not recognized",
                    }
                )
            )

    def permitted_document_accessed(self, event):
        data = event["data"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "permit.accessed",
                    "message": "Your permitted document was accessed.",
                    "data": data,
                }
            )
        )

    def disconnect(self, code):

        IdentityAccessPermit.objects.filter(channel_name=self.channel_name).delete()
        return super().disconnect(code)
