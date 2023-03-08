from django.urls import path, include
from gateway.views import GetDocumentsView, CheckNINView, LastUpdatedAtView

app_name = "gateway"
urlpatterns = [
    path("documents/", GetDocumentsView.as_view(), name="documents"),
    path("check/<str:NIN>/", CheckNINView.as_view(), name="check_nin"),
    path(
        "last-updated-at/<str:NIN>/",
        LastUpdatedAtView.as_view(),
        name="last_updated_at",
    ),
]
