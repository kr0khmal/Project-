from rest_framework import serializers
from .models import Booking
from listings.models import Listing


class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source="tenant.id")

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id", "tenant", "status", "created_at"]

    def validate(self, data):
        start = data["start_date"]
        end = data["end_date"]

        if start >= end:
            raise serializers.ValidationError("End date must be after start date.")

        return data

    def create(self, validated_data):
        validated_data["tenant"] = self.context["request"].user
        return super().create(validated_data)
