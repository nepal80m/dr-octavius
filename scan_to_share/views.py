from asgiref.sync import async_to_sync
import channels.layers

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from scan_to_share.serializers import (
    ScanRequestCreateSerializer,
    ScanRequestApproveSerializer,
)
from scan_to_share.models import ScanRequest
from django.shortcuts import get_object_or_404
import requests
from rest_framework.permissions import AllowAny
from gateway.views import fetch_all_documents

# Send by webapp to start new request session.
class ScanRequestCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ScanRequestCreateSerializer


class ScanRequestDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ScanRequest.objects.filter(is_active=True).all()
    lookup_field = "request_id"
    serializer_class = ScanRequestCreateSerializer


class ScanRequestApprovalView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ScanRequestApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        request_id = validated_data["request_id"]
        is_approved = validated_data["is_approved"]

        scan_request = get_object_or_404(
            ScanRequest, request_id=request_id, is_active=True
        )

        approved_data = {}
        for field in scan_request.requested_fields:
            approved_data[field] = None
        channel_layer = channels.layers.get_channel_layer()
        if is_approved:
            documents = fetch_all_documents(NIN=user.username)

            for document in documents:
                document_type = document["document_type"]
                document_details = document["document_details"]
                for field, field_value in document_details.items():
                    if field in approved_data:
                        approved_data[field] = field_value

        async_to_sync(channel_layer.group_send)(
            request_id,
            {
                "type": "request_approval",
                "message": "Your request is approved",
                "status": is_approved,
                "c": approved_data,
            },
        )

        scan_request.is_approved = is_approved
        scan_request.is_active = False
        scan_request.save()

        return Response(
            {
                "request_id": request_id,
                "is_approved": is_approved,
            }
        )


# class TestAPI(APIView):
#     permission_classes = [
#         AllowAny,
#     ]

#     def get(self, request, request_id, *args, **kwargs):
#         print(request_id)
#         channel_layer = channels.layers.get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             request_id,
#             {"type": "accept_request", "message": "Your request is approved"},
#         )
#         # send_event("test", "message", {"text": "hello world"})

#         return Response({"message": "Hello World!"})


# class ScanRequestApprovalCheckView(APIView):
#     def get(self, request, request_id, *args, **kwargs):
#         scan_request = get_object_or_404(ScanRequest, request_id=request_id)
#         return Response(
#             {
#                 "request_id": scan_request.request_id,
#                 "is_approved": scan_request.is_approved,
#             }
#         )


# class ScanRequestDetailsView(APIView):
#     def get(self, request, request_id, *args, **kwargs):
#         scan_request = get_object_or_404(ScanRequest, request_id=request_id)
#         response = {
#             "request_id": scan_request.request_id,
#             "is_approved": scan_request.is_approved,
#             "requested_fields": scan_request.requested_fields,
#             "approved_data": scan_request.approved_data,
#         }
#         scan_request.is_active = False
#         scan_request.save()

#         return Response(response)
