from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from listings.models import Listing


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListingReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        listing_id = self.kwargs["listing_id"]
        return Review.objects.filter(listing_id=listing_id)
