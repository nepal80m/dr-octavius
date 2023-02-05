# import imp
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.utils import timezone
from autho.models import OTPToken
from django.utils.translation import gettext_lazy as _
import requests

User = get_user_model()

# from django.contrib.auth import get_user_model

# User = get_user_model()
# # Create your serializers here.
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "fname", "lname", "phone", "email", "address", "image", "image"]
#         extra_kwargs = {
#             "id": {"read_only": True},
#             "fname": {"required": True},
#             "lname": {"required": True},
#             "phone": {"required": True},
#             "email": {"required": True},
#         }


# def create(self, validated_data):
#     user = User.objects.create(**validated_data)
#     return user


class GenerateOTPSerializer(serializers.Serializer):
    NIN = serializers.CharField(max_length=64)
    mobile_number = PhoneNumberField(
        region="NP",
        max_length=15,
    )

    # def validate(self, data):
    #     NIN = data["NIN"]
    #     mobile = data["mobile"]
    #     return self.super().validate(data)

    def create(self, validated_data):
        # TODO: Create separate apis to register user and generate OTP.

        username = validated_data["NIN"]
        mobile_number = validated_data["mobile_number"]
        try:
            user = User.objects.get(username=username, mobile_number=mobile_number)
        except User.DoesNotExist:
            user = User.objects.create(username=username, mobile_number=mobile_number)
            user.set_unusable_password()
            user.save()

        # TODO: Make the signal do this work.
        # OTPToken.objects.active().filter(user=user).update(is_active=False)
        OTPToken.objects.filter(user=user).delete()

        otp_token = OTPToken.objects.create(user=user)

        self.validated_data["user"] = user
        self.validated_data["otp_token"] = otp_token
        return user


# class OTPField(serializers.CharField):
#     default_error_messages = {
#         "max_length": _("Tokens are {max_length} digits long."),
#         "min_length": _("Tokens are {min_length} digits long."),
#     }


def validate_otp_age(otp):
    """
    Returns True if a given token is within the age expiration limit.
    """

    try:
        token = OTPToken.objects.get(otp=otp, is_active=True)
        seconds = (timezone.now() - token.created_at).total_seconds()
        token_expiry_time = 15 * 60  # 15 minutes
        # if token.user.pk in api_settings.PASSWORDLESS_DEMO_USERS.keys():
        #     return True
        if seconds <= token_expiry_time:
            return True
        else:
            # Invalidate our token.
            token.is_active = False
            # TODO: Or token.delete()
            token.save()
            return False

    except OTPToken.DoesNotExist:
        # No valid otp.
        return False


def otp_age_validator(value):
    """
    Check token age
    Makes sure a token is within the proper expiration datetime window.
    """
    valid_token = validate_otp_age(value)
    if not valid_token:
        raise serializers.ValidationError("The token you entered isn't valid.")
    return value


class OTPAuthSerializer(serializers.Serializer):

    """
    Abstract class inspired by DRF's own token serializer.
    Returns a user if valid, None or a message if not.
    """

    NIN = serializers.CharField(max_length=64)
    mobile_number = PhoneNumberField(
        region="NP",
        max_length=15,
    )
    otp = serializers.CharField(
        min_length=4, max_length=4, validators=[otp_age_validator]
    )

    def validate(self, data):
        validated_data = super().validate(data)
        username = validated_data["NIN"]
        mobile_number = validated_data["mobile_number"]
        opt = data.get("otp")
        print(f"Received OTP: {opt} to verify {username} and {mobile_number}")
        try:
            user = User.objects.get(username=username, mobile_number=mobile_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        try:
            otp_token = OTPToken.objects.get(user=user, otp=opt, is_active=True)
        except OTPToken.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data["user"] = user
        data["otp_token"] = otp_token
        return data

    def save(self):
        user = self.validated_data["user"]
        user.mobile_number_verified = True
        user.save()
        return user


class TokenResponseSerializer(serializers.Serializer):
    """
    Our default response serializer.
    """

    token = serializers.CharField(source="key")
    key = serializers.CharField(write_only=True)
