import requests
import datetime
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
import card_generator

User = get_user_model()


def fetch_NID(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    nid_url = settings.POCHITA_BASE_URL + f"nid/{NIN}/"

    nid_result = requests.get(nid_url, headers=headers)
    nid_status_code = nid_result.status_code
    if nid_status_code != 200:
        nid = None
    else:
        nid = nid_result.json()

    return nid


def fetch_NID_latest_update_date(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    nid_url = settings.POCHITA_BASE_URL + f"nid/last-updated-date/{NIN}/"

    nid_result = requests.get(nid_url, headers=headers)
    nid_status_code = nid_result.status_code
    if nid_status_code != 200:
        return None
    else:
        return nid_result.json()


def fetch_CTZ(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    ctz_url = settings.POCHITA_BASE_URL + f"ctz/{NIN}/"

    ctz_result = requests.get(ctz_url, headers=headers)
    ctz_status_code = ctz_result.status_code
    if ctz_status_code != 200:
        ctz = None
    else:
        ctz = ctz_result.json()

    return ctz


def fetch_CTZ_latest_update_date(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    ctz_url = settings.POCHITA_BASE_URL + f"ctz/last-updated-date/{NIN}/"

    ctz_result = requests.get(ctz_url, headers=headers)
    ctz_status_code = ctz_result.status_code
    if ctz_status_code != 200:
        return None
    else:
        return ctz_result.json()


def fetch_DVL(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    dvl_url = settings.POCHITA_BASE_URL + f"dvl/{NIN}/"

    dvl_result = requests.get(dvl_url, headers=headers)
    dvl_status_code = dvl_result.status_code
    if dvl_status_code != 200:
        dvl = None
    else:
        dvl = dvl_result.json()

    return dvl


def fetch_DVL_latest_update_date(token, NIN):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    dvl_url = settings.POCHITA_BASE_URL + f"dvl/last-updated-date/{NIN}/"

    dvl_result = requests.get(dvl_url, headers=headers)
    dvl_status_code = dvl_result.status_code
    if dvl_status_code != 200:
        return None
    else:
        return dvl_result.json()


# def fetch_all_documents(NIN):

#     try:
#         pochita_token_config = get_object_or_404(
#             CoreConfig, app="core", key="pochita_token"
#         )
#         token = pochita_token_config.value
#     except Http404:
#         print("Pochita token was not found.")
#         return Response(
#             {"message": "Something went wrong."},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )
#     nid = fetch_NID(token, NIN)
#     ctz = fetch_CTZ(token, NIN)
#     dvl = fetch_DVL(token, NIN)

#     documents = {"NID": nid, "CTZ": ctz, "DVL": dvl}

#     return documents


def fetch_documents(NIN: str, documents: list[str] = [], fetch_all: bool = False):

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
    fetched_documents = {}
    if fetch_all or ("NID" in documents):
        nid = fetch_NID(token, NIN)
        if nid is not None:
            nid_card_front = card_generator.generate_nid_front(nid)
            nid_card_back = card_generator.generate_nid_back(nid)
            nid["card_front"] = nid_card_front
            nid["card_back"] = nid_card_back

        fetched_documents["NID"] = nid

    if fetch_all or ("CTZ" in documents):
        ctz = fetch_CTZ(token, NIN)
        if ctz is not None:
            ctz_card_front = card_generator.generate_ctz_front(ctz)
            ctz_card_back = card_generator.generate_ctz_back(ctz)
            ctz["card_front"] = ctz_card_front
            ctz["card_back"] = ctz_card_back
        fetched_documents["CTZ"] = ctz

    if fetch_all or ("DVL" in documents):
        dvl = fetch_DVL(token, NIN)
        if dvl is not None:
            dvl_card_front = card_generator.generate_dvl_front(dvl)
            dvl_card_back = card_generator.generate_dvl_back(dvl)
            dvl["card_front"] = dvl_card_front
            dvl["card_back"] = dvl_card_back
        fetched_documents["DVL"] = dvl

    return fetched_documents


def fetch_documents_latest_update_date(
    NIN: str, documents: list[str] = [], fetch_all: bool = False
):

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
    fetched_documents_latest_update_date = {}
    if fetch_all or ("NID" in documents):
        nid = fetch_NID_latest_update_date(token, NIN)
        if nid is not None:
            fetched_documents_latest_update_date["NID"] = nid["updatedAt"]

    if fetch_all or ("CTZ" in documents):
        ctz = fetch_CTZ_latest_update_date(token, NIN)
        if ctz is not None:
            fetched_documents_latest_update_date["CTZ"] = ctz["updatedAt"]

    if fetch_all or ("DVL" in documents):
        dvl = fetch_DVL_latest_update_date(token, NIN)
        if dvl is not None:
            fetched_documents_latest_update_date["DVL"] = dvl["updatedAt"]

    return fetched_documents_latest_update_date


# This view is used to get all the documents of a user.
class GetDocumentsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        NIN = user.username

        # Getting the Pochita token from the database

        try:
            # documents = fetch_all_documents(NIN)
            documents = fetch_documents(NIN=NIN, fetch_all=True)
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


class LastUpdatedAtView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, NIN, *args, **kwargs):
        user = request.user
        NIN = user.username
        print(request.headers)
        print(request.META)
        print(f"Got request for last updated at by {NIN}")

        try:
            last_updated_at = fetch_documents_latest_update_date(
                NIN=NIN, fetch_all=True
            )
        except Exception as e:
            print(e)
            print("Couldn't fetch the documents latest update date")
            return Response(
                {"message": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        max_date = max(
            [
                datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
                for date in last_updated_at.values()
            ]
        )

        return Response(
            {
                "NIN": user.username,
                "last_updated_at": max_date,
            }
        )
