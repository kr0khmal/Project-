from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.db.models import Count
from .models import ListingView
from .serializers import ListingViewSerializer
from listings.models import Listing


class RegisterViewView(APIView):
    """
    POST: /api/analytics/view/
    { "listing_id": 5 }
    Сохраняет факт просмотра объявления
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        listing_id = request.data.get("listing_id")
        if not listing_id:
            return Response({"error": "listing_id required"}, status=400)

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=404)

        user = request.user if request.user.is_authenticated else None

        ListingView.objects.create(listing=listing, user=user)

        return Response({"status": "view_saved"})


class PopularListingsView(APIView):
    """
    GET: /api/analytics/popular/
    Вывод популярных объявлений по количеству просмотров
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        popular = (
            Listing.objects.annotate(view_count=Count("views"))
            .order_by("-view_count")
            .values("id", "title", "view_count")
        )
        return Response(list(popular))


class UserViewsHistoryView(generics.ListAPIView):
    """
    GET: /api/analytics/my/
    История просмотров пользователя
    """
    serializer_class = ListingViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ListingView.objects.filter(user=self.request.user).order_by("-viewed_at")
