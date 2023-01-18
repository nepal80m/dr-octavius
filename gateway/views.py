import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import Http404
from core.models import CoreConfig

User = get_user_model()


def fetch_all_documents(NIN):

    try:
        pochita_token_config = get_object_or_404(
            CoreConfig, app="core", key="pochita_token"
        )
        token = pochita_token_config.value
    except Http404:
        print("Pochita token was not found.")
        return Response(
            {"message": "Something went wrong."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    nid_url = settings.POCHITA_BASE_URL + f"nid/{NIN}/"

    headers = {
        "Authorization": f"Bearer {token}",
    }
    nid_result = requests.get(nid_url, headers=headers)
    nid_status_code = nid_result.status_code
    nid = nid_result.json()

    documents = [
        {
            "document_type": "NID",
            "document_details": nid,
        },
    ]
    return documents


# This view is used to get all the documents of a user.
class GetDocumentsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        NIN = user.username

        # Getting the Pochita token from the database

        try:
            documents = fetch_all_documents(NIN)
        except Exception as e:
            print(e)
            print("Couldn't fetch the documents")
            return Response(
                {"message": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "NIN": user.username,
                "documents": documents,
            }
        )

        # print(status_code)
        # print(result)
        # if status_code is not 200:
        #     return Response(
        #         {"message": "Invalid NIN."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )


# This view is used to check if NIN exists or not.
class CheckNINView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, NIN, *args, **kwargs):
        # user = get_object_or_404(User, username=NIN)
        # Getting the Pochita token from the database
        try:
            pochita_token_config = get_object_or_404(
                CoreConfig, app="core", key="pochita_token"
            )
            token = pochita_token_config.value
        except Http404:
            print("Pochita token was not found.")
            return Response(
                {"message": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        headers = {"Authorization": f"Bearer {token}"}
        # response = {"NIN": user.username, "documents": []}

        nid_url = settings.POCHITA_BASE_URL + f"nid/check/{NIN}"

        result = requests.get(nid_url, headers=headers)
        status_code = result.status_code
        print(status_code)
        if status_code != 200:
            return Response(
                {
                    "NIN": NIN,
                    "exists": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            return Response(
                {
                    "NIN": NIN,
                    "exists": True,
                },
                status=status.HTTP_200_OK,
            )
