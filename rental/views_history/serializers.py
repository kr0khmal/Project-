from rest_framework import serializers
from .models import ViewRecord


class ViewRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewRecord
        fields = "__all__"
        read_only_fields = ["id", "count", "last_viewed", "user"]
