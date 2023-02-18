from django.urls import path, include
from gateway.views import GetDocumentsView, CheckNINView

app_name = "gateway"
urlpatterns = [
    path("documents/", GetDocumentsView.as_view(), name="documents"),
    path("check/<str:NIN>/", CheckNINView.as_view(), name="check_nin"),
]
