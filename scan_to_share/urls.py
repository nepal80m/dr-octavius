from django.contrib import admin
from django.urls import path, include
from scan_to_share.views import (
    ScanRequestCreateView,
    ScanRequestDetailView,
    ScanRequestApprovalView,
)
from rest_framework import routers

router = routers.DefaultRouter()


app_name = "scan_to_share"
urlpatterns = [
    path("", ScanRequestCreateView.as_view(), name="create"),
    path(
        "<str:request_id>/",
        ScanRequestDetailView.as_view(),
        name="details",
    ),
    path(
        "<str:request_id>/approval/",
        ScanRequestApprovalView.as_view(),
        name="approve",
    ),
    # path(
    #     "test/<str:request_id>/",
    #     TestAPI.as_view(),
    # ),
    # path(
    #     "check/<str:request_id>",
    #     ScanRequestApprovalCheckView.as_view(),
    #     name="check_approval",
    # ),
]
