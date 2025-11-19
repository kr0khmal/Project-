from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ViewRecord
from .serializers import ViewRecordSerializer
from rental.models import Listing


class SaveViewRecordView(APIView):
    """
    POST: {"listing_id": 1}
    Сохраняет просмотр объявления
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        listing_id = request.data.get("listing_id")

        if not listing_id:
            return Response({"error": "listing_id is required."}, status=400)

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({"error": "Listing does not exist."}, status=404)

        user = request.user if request.user.is_authenticated else None

        obj, created = ViewRecord.objects.get_or_create(
            user=user,
            listing=listing
        )

        if not created:
            obj.count += 1
            obj.save()

        return Response({"status": "saved", "listing_id": listing_id})


class PopularListingsView(APIView):
    """
    GET — список объявлений с наибольшим количеством просмотров
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        listings = Listing.objects.all()
        data = []

        for listing in listings:
            views = listing.views.aggregate(total=models.Sum("count"))["total"] or 0
            data.append({
                "id": listing.id,
                "title": listing.title,
                "total_views": views
            })

        sorted_data = sorted(data, key=lambda x: x["total_views"], reverse=True)

        return Response(sorted_data)


class UserViewHistoryView(generics.ListAPIView):
    """
    GET — история просмотров пользователя
    """
    serializer_class = ViewRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ViewRecord.objects.filter(user=self.request.user).order_by("-last_viewed")
