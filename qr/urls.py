from django.contrib import admin
from django.urls import path, include
from qr.views import (
    # IdentityAccessRequestCreateView,
    IdentityAccessRequestDetailView,
    IdentityAccessRequestApprovalView,
    IdentityAccessPermitCreateView,
    AccessPermittedIdentityView,
)
from rest_framework import routers

router = routers.DefaultRouter()


app_name = "qr"
urlpatterns = [
    # path("", IdentityAccessRequestCreateView.as_view(), name="create"),
    path(
        "request/<str:request_id>/",
        IdentityAccessRequestDetailView.as_view(),
        name="request_details",
    ),
    path(
        "request/<str:request_id>/approval/",
        IdentityAccessRequestApprovalView.as_view(),
        name="request_approval",
    ),
    path(
        "permit/",
        IdentityAccessPermitCreateView.as_view(),
        name="create_permit",
    ),
    path(
        "permit/<str:permit_id>/",
        AccessPermittedIdentityView.as_view(),
        name="access_permitted_identity",
    ),
    # path(
    #     "test/<str:request_id>/",
    #     TestAPI.as_view(),
    # ),
    # path(
    #     "check/<str:request_id>",
    #     IdentityViewRequestApprovalCheckView.as_view(),
    #     name="check_approval",
    # ),
]
