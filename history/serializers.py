from rest_framework import serializers
from history.models import ActivityHistory
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests


class ActivityHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityHistory
        fields = (
            "activity",
            "title",
            "description",
            "extra_info",
            "created_at",
            "modified_at",
        )
