from rest_framework import serializers
from .models import Listing, ListingView


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "views_count"]


class ListingDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "views_count"]
