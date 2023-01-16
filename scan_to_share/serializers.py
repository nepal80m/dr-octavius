from rest_framework import serializers
from scan_to_share.models import ScanRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests


class ScanRequestCreateSerializer(serializers.Serializer):
    request_id = serializers.CharField()
    requester = serializers.CharField(max_length=100)
    requested_fields = serializers.ListField()

    def create(self, validated_data):
        return ScanRequest.objects.create(**validated_data)

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # requester = models.CharField(max_length=100)
    # request_time = models.DateTimeField(auto_now_add=True)
    # requested_fields = models.JSONField()
    # approved_data = models.JSONField()
    # is_approved = models.BooleanField(default=False)


class ScanRequestApproveSerializer(serializers.Serializer):
    request_id = serializers.CharField()
    is_approved = serializers.BooleanField()

    # def create(self, validated_data):
    #     scan_request = get_object_or_404(
    #         ScanRequest, request_id=str(validated_data["request_id"])
    #     )
    #     if validated_data["is_approved"]:
    #         # TODO: FIX this..
    #         # response = requests.get("http://localhost:3000/", verify=False)
    #         # print(response)
    #         # print(response.content.decode())
    #         scan_request.is_approved = True
    #         scan_request.save()
    #     else:
    #         scan_request.delete()
    #     return Response(
    #         {
    #             "request_id": validated_data["request_id"],
    #             "is_approved": validated_data["is_approved"],
    #         }
    #     )
