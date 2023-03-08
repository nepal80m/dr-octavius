from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView
from history.models import ActivityHistory
from history.serializers import ActivityHistorySerializer

# Create your views here.


class ActivityHistoryListCreateView(ListCreateAPIView):
    serializer_class = ActivityHistorySerializer

    def get_queryset(self):
        return ActivityHistory.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        activity_history = serializer.save(user=self.request.user)
