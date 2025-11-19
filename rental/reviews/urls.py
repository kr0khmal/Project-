from django.urls import path
from .views import ReviewCreateView, ListingReviewsView

urlpatterns = [
    path("create/", ReviewCreateView.as_view()),
    path("listing/<int:listing_id>/", ListingReviewsView.as_view()),
]
