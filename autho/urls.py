from django.urls import path, include

# from auth.views import *
# from rest_framework import routers

# # from knox.views import LogoutView

# router = routers.DefaultRouter()
# router.register(r"user-register", RegisterView, basename="task")
# urlpatterns = [
#     path("", include(router.urls)),
#     # path("logout/", LogoutView.as_view(), name="knox_logout"),
# ]


# from drfpasswordless.settings import api_settings
# from django.urls import path
# from drfpasswordless.views import (
#      ObtainEmailCallbackToken,
#      ObtainMobileCallbackToken,
#      ObtainAuthTokenFromCallbackToken,
#      VerifyAliasFromCallbackToken,
#      ObtainEmailVerificationCallbackToken,
#      ObtainMobileVerificationCallbackToken,
# )
from autho.views import GenerateOTPView, OTPAuthView

app_name = "autho"

urlpatterns = [
    path("", GenerateOTPView.as_view(), name="generate_otp"),
    path("verify/", OTPAuthView.as_view(), name="auth_token"),
]
