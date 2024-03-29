import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from autho.serializers import (
    GenerateOTPSerializer,
    OTPAuthSerializer,
    TokenResponseSerializer,
)
from core.models import CoreConfig
from autho.models import OTPToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404
from history.models import ActivityHistory
from history.constants import LOGGED_IN

# from rest_framework import viewsets
# from django.contrib.auth import get_user_model
# from auth.serializers import RegisterSerializer
# from knox.models import AuthToken
# from django.contrib.auth import login
# from rest_framework import permissions, generics, status
# import requests

# User = get_user_model()
# # Create your views here.
# class RegisterView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer


# def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     self.perform_create(serializer)
#     headers = self.get_success_headers(serializer.data)
#     return Response(
#         {
#             "response": serializer.data,
#             "scucess": True,
#             "message": "User created successfully",
#             "status": status.HTTP_201_CREATED,
#         }
#     )


def send_sms_with_otp(mobile_number, otp):
    """
    Sends a SMS to user.mobile_number via Twilio.

    Passes silently without sending in test environment.
    """

    print(f"Sending OTP to {mobile_number} via Twilio: {otp}")
    print(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # return True

    try:
        if not "9851228881" in mobile_number:
            return True
        # if api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER:
        #     # We need a sending number to send properly

        from twilio.rest import Client

        twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        twilio_client.messages.create(
            body=f"This is your login OTP for Parichaya App: {otp}.",
            from_=settings.TWILIO_NOREPLY_NUMBER,
            to=mobile_number,
        )
        return True

    except Exception as e:
        print(e)
        return False


class GenerateOTPView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        print("Received request to generate OTP")
        serializer = GenerateOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            NIN = serializer.validated_data["NIN"]
            mobile_number = serializer.validated_data["mobile_number"]
            print(f"Validated NIN:{NIN} and mobile number:{mobile_number}")
            # Make query to the blockchain to check if the NIN is valid.
            url = settings.POCHITA_BASE_URL + f"nid/{NIN}/"
            # Getting the Pochita token from the database
            try:
                pochita_token_config = get_object_or_404(
                    CoreConfig, app="core", key="pochita_token"
                )
                print("Retrieved Pochita token")
            except Http404:
                print("Pochita token was not found")
                return Response(
                    {"message": "Something went wrong."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            token = pochita_token_config.value

            headers = {
                "Authorization": f"Bearer {token}",
            }

            # Getting the NIN details from the blockchain
            try:
                print("Sending request to blockchain")
                response = requests.get(url, headers=headers)
                status_code = response.status_code
                result = response.json()
                print(f"Got response with status code:", status_code)
                # print(result)
                if status_code != 200:
                    return Response(
                        {"message": "Invalid NIN."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                print(e)
                return Response(
                    {"message": "Something went wrong."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Checking if the requested mobile number matches the registered mobile number
            trimmed_mobile_number = mobile_number.as_e164
            if result["mobile_number"] != trimmed_mobile_number:
                return Response(
                    {"message": "Invalid mobile number."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            """



            # TODO: Check if the user is already registered and has the matching mobile number.
            if mobile number is different:
                expire all the auth tokens for the user.
                update the mobile number and proceed to send OTP to the new mobile.
            """

            serializer.save()  # Generate OTP
            user = serializer.validated_data["user"]
            otp_token = serializer.validated_data["otp_token"]
            # TODO: Send OTP
            success = send_sms_with_otp(user.mobile_number.as_e164, otp_token.otp)
            """
            to: user.mobile,
            message: "This is your login OTP for Parichaya App: {token} for."
            """
            # Respond With Success Or Failure of Sent
            if success:
                return Response(
                    {"message": "OTP sent to registered mobile."},
                    status=status.HTTP_200_OK,
                )
            else:
                otp_token.delete()
                return Response(
                    {"message": "Unable to send OTP to mobile."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # TODO: can remove if else.
        else:
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )


class OTPAuthView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        headers = request.headers
        device_model = headers.get("Model", "Unknown")
        device_os = headers.get("Os", "Unknown")
        # print(request["os"])
        serializer = OTPAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            otp_token = serializer.validated_data["otp_token"]
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            otp_token.delete()
            response = {
                "token": token.key,
            }
            ActivityHistory.objects.create(
                user=user,
                activity=LOGGED_IN.activity_code,
                description=LOGGED_IN.description.format(
                    device=f"{device_model} ({device_os.capitalize()})"
                ),
            )

            print(f"Created logged in activity history.")

            print(f"Verified and sending auth token back. {token.key}")
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Couldn't log you in. Try again later."},
                status=status.HTTP_400_BAD_REQUEST,
            )
