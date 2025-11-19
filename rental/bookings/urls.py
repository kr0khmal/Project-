from django.urls import path
from .views import (
    BookingCreateView,
    BookingListView,
    BookingCancelView,
    LandlordBookingList,
    BookingApproveView,
    BookingRejectView,
)

urlpatterns = [
    path("create/", BookingCreateView.as_view()),
    path("my/", BookingListView.as_view()),
    path("<int:pk>/cancel/", BookingCancelView.as_view()),

    path("landlord/", LandlordBookingList.as_view()),
    path("<int:pk>/approve/", BookingApproveView.as_view()),
    path("<int:pk>/reject/", BookingRejectView.as_view()),
]
