from rest_framework import serializers
from .models import Review
from bookings.models import Booking
from django.utils import timezone


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]

    def validate_rating(self, rating):
        if rating < 1 or rating > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return rating

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        listing = data["listing"]

        # Проверяем, есть ли у пользователя завершённое бронирование
        completed_bookings = Booking.objects.filter(
            tenant=user,
            listing=listing,
            status="approved",
            end_date__lt=timezone.now().date()
        )

        if not completed_bookings.exists():
            raise serializers.ValidationError(
                "You can leave a review only after completing an approved booking."
            )

        # Один отзыв на одно объявление
        if Review.objects.filter(user=user, listing=listing).exists():
            raise serializers.ValidationError("You have already reviewed this listing.")

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
