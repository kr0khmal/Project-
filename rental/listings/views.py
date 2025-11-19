from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing, ListingView
from .serializers import ListingSerializer, ListingDetailSerializer
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q, Count


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["location", "housing_type", "rooms"]
    ordering_fields = ["price", "created_at", "views_count"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # цена: min_price / max_price
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # сортировка по популярности
        popular = self.request.query_params.get("popular")
        if popular:
            queryset = queryset.order_by("-views_count")

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()

        if request.user.is_authenticated:
            # увеличиваем счётчик
            listing.views_count += 1
            listing.save()

            # сохраняем в историю просмотров
            ListingView.objects.create(user=request.user, listing=listing)

        return super().retrieve(request, *args, **kwargs)
