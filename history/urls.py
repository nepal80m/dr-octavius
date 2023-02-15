from django.contrib import admin
from django.urls import path, include
from history.views import ActivityHistoryListCreateView
from rest_framework import routers

app_name = "history"
urlpatterns = [
    path(
        "",
        ActivityHistoryListCreateView.as_view(),
        name="activity_history",
    ),
]
