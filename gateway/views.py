import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

User = get_user_model()


def fetch_all_documents(NIN):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFzaW1uZXBhbCIsImlkIjoiNjNjMmQ0YjhlODlhOTU3MGFkMDMxZWU4IiwiaWF0IjoxNjczNzEyODI1fQ.ttXWpdGdJovelBMLWhbNnNRUE8vrXVZlBNL1_bV7bHk"
    }
    nid_url = f"http://localhost:3000/nid/{NIN}"

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
        documents = fetch_all_documents(NIN)
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
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFzaW1uZXBhbCIsImlkIjoiNjNjMmQ0YjhlODlhOTU3MGFkMDMxZWU4IiwiaWF0IjoxNjczNzEyODI1fQ.ttXWpdGdJovelBMLWhbNnNRUE8vrXVZlBNL1_bV7bHk"
        }
        # response = {"NIN": user.username, "documents": []}

        nid_url = f"http://localhost:3000/nid/check/{NIN}"

        result = requests.get(nid_url, headers=headers)
        status_code = result.status_code
        print(status_code)
        if status_code is not 200:
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
