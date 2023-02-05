from django.urls import re_path

from qr.consumers import IdentityAccessRequestConsumer, IdentityAccessPermitConsumer

websocket_urlpatterns = [
    re_path(r"ws/qr/request/", IdentityAccessRequestConsumer.as_asgi()),
    re_path(r"ws/qr/permit/", IdentityAccessPermitConsumer.as_asgi()),
]
