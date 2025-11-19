from rest_framework import generics, permissions
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsTenant, IsLandlord


class BookingCreateView(generics.CreateAPIView):
    """
    Создать бронирование — только арендатор
    """
    serializer_class = BookingSerializer
    permission_classes = [IsTenant]


class BookingListView(generics.ListAPIView):
    """
    Просмотр своих бронирований (арендатор)
    """
    serializer_class = BookingSerializer
    permission_classes = [IsTenant]

    def get_queryset(self):
        return Booking.objects.filter(tenant=self.request.user)


class BookingCancelView(generics.UpdateAPIView):
    """
    Отмена бронирования
    """
    serializer_class = BookingSerializer
    permission_classes = [IsTenant]

    def get_queryset(self):
        return Booking.objects.filter(tenant=self.request.user)

    def perform_update(self, serializer):
        booking = self.get_object()

        # нельзя отменять после начала проживания
        if timezone.now().date() >= booking.start_date:
            raise ValueError("Booking cannot be canceled after start date.")

        serializer.save(status="canceled")


class LandlordBookingList(generics.ListAPIView):
    """
    Арендодатель видит заявки по своим объявлениям
    """
    serializer_class = BookingSerializer
    permission_classes = [IsLandlord]

    def get_queryset(self):
        return Booking.objects.filter(listing__owner=self.request.user)


class BookingApproveView(generics.UpdateAPIView):
    """
    Подтверждение бронирования
    """
    serializer_class = BookingSerializer
    permission_classes = [IsLandlord]

    def get_queryset(self):
        return Booking.objects.filter(listing__owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(status="approved")


class BookingRejectView(generics.UpdateAPIView):
    """
    Отклонение бронирования
    """
    serializer_class = BookingSerializer
    permission_classes = [IsLandlord]

    def get_queryset(self):
        return Booking.objects.filter(listing__owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(status="rejected")
