from __future__ import unicode_literals
import string
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from autho.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=255, unique=True)  # hashed NIN or plain NIN
    mobile_number = PhoneNumberField(region="NP", max_length=15)
    mobile_number_verified = models.BooleanField(default=False)
    # name = models.CharField(max_length=255)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.username, self.mobile_number)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


def generate_numeric_token():
    """
    Generate a random 6 digit string of numbers.
    We use this formatting to allow leading 0s.
    """
    return get_random_string(length=4, allowed_chars=string.digits)


class OTPTokenManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def inactive(self):
        return self.get_queryset().filter(is_active=False)


class OTPToken(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    otp = models.CharField(max_length=4, default=generate_numeric_token)

    objects = OTPTokenManager()

    def __str__(self):
        return self.otp
