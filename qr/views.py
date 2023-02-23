from asgiref.sync import async_to_sync
import channels.layers

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from qr.serializers import (
    IdentityAccessRequestApprovalSerializer,
    IdentityAccessRequestSerializer,
    IdentityAccessPermitSerializer,
)
from qr.models import IdentityAccessRequest, IdentityAccessPermit
from django.shortcuts import get_object_or_404
import requests
from rest_framework.permissions import AllowAny
from gateway.views import fetch_documents
from history.models import ActivityHistory
from history.constants import (
    QR_SCANNED,
    APPROVED_ACCESS_REQUEST,
    VIEWED_SHARED_DETAILS,
    DOCUMENT_CODE_DVL,
    DOCUMENT_CODE_AGE,
)

# Send by webapp to start new request session.
# class IdentityAccessRequestCreateView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = IdentityViewRequestCreateSerializer


class IdentityAccessRequestDetailView(RetrieveAPIView):
    # permission_classes = [AllowAny]
    queryset = IdentityAccessRequest.objects.filter(is_active=True).all()
    lookup_field = "request_id"
    serializer_class = IdentityAccessRequestSerializer

    def retrieve(self, request, request_id, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        user = request.user
        ActivityHistory.objects.create(
            user=user,
            activity=QR_SCANNED.activity_code,
            description=QR_SCANNED.description.format(
                source=f"{instance.requester.name} ({instance.requester.domain})"
            ),
        )

        return Response(serializer.data)


class IdentityAccessRequestApprovalView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        print(f"Received approval request from {user.username}")

        serializer = IdentityAccessRequestApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        request_id = validated_data["request_id"]
        is_approved = validated_data["is_approved"]
        print(f"Approval for request {request_id} is {is_approved}")

        access_request = get_object_or_404(
            IdentityAccessRequest, request_id=request_id, is_active=True
        )
        channel_layer = channels.layers.get_channel_layer()

        print("Sending approval to socket")
        async_to_sync(channel_layer.send)(
            access_request.channel_name,
            {
                "type": "access_request_approval",
                "status": is_approved,
            },
        )

        if not is_approved:
            print("Access request was rejected.")
            return Response(
                {"message": "Access request was rejected."},
                status=status.HTTP_200_OK,
            )

        print("Access request was approved.")
        approved_data = {}
        # for field in access_request.requester.requested_fields:
        #     approved_data[field] = None
        if is_approved:
            # documents = fetch_all_documents(NIN=user.username)
            documents = fetch_documents(NIN=user.username, fetch_all=True)

            for field in access_request.requester.requested_fields:
                doc_type = "NID"
                if field.startswith("CTZ_"):
                    doc_type = "CTZ"
                if field.startswith("DVL_"):
                    doc_type = "DVL"
                document = documents[doc_type]

                if document is not None:
                    approved_data[field] = document.get(field)
                else:
                    approved_data[field] = None

            # for document in documents:
            #     document_type = document["document_type"]
            #     document_details = document["document_details"]
            #     for field, field_value in document_details.items():
            #         if field in approved_data:
            #             approved_data[field] = field_value
        print("Sending approved data to socket")

        async_to_sync(channel_layer.send)(
            access_request.channel_name,
            {
                "type": "send_requested_data",
                "data": approved_data,
            },
        )

        # async_to_sync(channel_layer.group_send)(
        #     request_id,
        #     {
        #         "type": "request_approval",
        #         "status": is_approved,
        #         "data": approved_data,
        #     },
        # )

        # access_request.is_approved = is_approved
        # access_request.is_active = False
        # access_request.save()

        access_request.delete()

        ActivityHistory.objects.create(
            user=user,
            activity=APPROVED_ACCESS_REQUEST.activity_code,
            description=APPROVED_ACCESS_REQUEST.description.format(
                requester=f"{access_request.requester.name} ({access_request.requester.domain})"
            ),
            extra_info={"fields": access_request.requester.requested_fields},
        )

        return Response(
            {
                "request_id": request_id,
                "is_approved": is_approved,
            }
        )


class IdentityAccessPermitCreateView(CreateAPIView):
    serializer_class = IdentityAccessPermitSerializer

    def perform_create(self, serializer):
        access_permit = serializer.save(permitted_by=self.request.user)


class AccessPermittedIdentityView(APIView):
    def get(self, request, permit_id, *args, **kwargs):
        user = request.user
        access_permit = get_object_or_404(IdentityAccessPermit, permit_id=permit_id)
        permitted_by = access_permit.permitted_by
        permitted_document_code = access_permit.permitted_document_code
        # permitted_data = {}
        # access_permit.delete()

        documents = fetch_documents(NIN=user.username, documents=["NID"])
        nid = documents["NID"]
        first_name = nid.get("first_name")
        middle_name = nid.get("middle_name")
        last_name = nid.get("last_name")

        if middle_name is None:
            full_name = f"{first_name} {last_name}"
        else:
            full_name = f"{first_name} {middle_name} {last_name}"

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.send)(
            access_permit.channel_name,
            {
                "type": "permitted_document_accessed",
                "data": {"viewer": full_name},
            },
        )
        if permitted_document_code == "DVL":
            documents = fetch_documents(NIN=permitted_by.username, documents=["DVL"])
            dvl = documents["DVL"]

            ActivityHistory.objects.create(
                user=permitted_by,
                activity=VIEWED_SHARED_DETAILS.activity_code,
                description=VIEWED_SHARED_DETAILS.description.format(
                    viewer=full_name,
                    document=DOCUMENT_CODE_DVL,
                ),
                extra_info={"fields": list(dvl.keys())},
            )
            return Response(
                {
                    "permitted_document_code": permitted_document_code,
                    "permitted_document": dvl,
                }
            )
        if permitted_document_code == "AGE":
            documents = fetch_documents(NIN=permitted_by.username, documents=["NID"])
            nid = documents["NID"]
            permitted_document = {
                "NIN": nid.get("NIN"),
                "face_image": nid.get("face_image"),
                "first_name": nid.get("first_name"),
                "middle_name": nid.get("middle_name"),
                "last_name": nid.get("last_name"),
                "dob": nid.get("dob"),
            }
            ActivityHistory.objects.create(
                user=permitted_by,
                activity=VIEWED_SHARED_DETAILS.activity_code,
                description=VIEWED_SHARED_DETAILS.description.format(
                    viewer=full_name,
                    document=DOCUMENT_CODE_AGE,
                ),
                extra_info={"fields": list(permitted_document.keys())},
            )
            return Response(
                {
                    "permitted_document_code": permitted_document_code,
                    "permitted_document": permitted_document,
                }
            )

        return Response(
            {
                "message": "Invalid document code",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

        # documents = fetch_documents(NIN=permitted_by.username, fetch_all=True)
        # permitted_data = documents.get(permitted_document)
        # return Response(
        #     {
        #         permitted_document: permitted_data,
        #     }
        # )


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


# class IdentityViewRequestApprovalCheckView(APIView):
#     def get(self, request, request_id, *args, **kwargs):
#         scan_request = get_object_or_404(IdentityViewRequest, request_id=request_id)
#         return Response(
#             {
#                 "request_id": scan_request.request_id,
#                 "is_approved": scan_request.is_approved,
#             }
#         )


# class IdentityViewRequestDetailsView(APIView):
#     def get(self, request, request_id, *args, **kwargs):
#         scan_request = get_object_or_404(IdentityViewRequest, request_id=request_id)
#         response = {
#             "request_id": scan_request.request_id,
#             "is_approved": scan_request.is_approved,
#             "requested_fields": scan_request.requested_fields,
#             "approved_data": scan_request.approved_data,
#         }
#         scan_request.is_active = False
#         scan_request.save()

#         return Response(response)
