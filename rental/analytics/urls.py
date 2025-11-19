from django.urls import path
from .views import RegisterViewView, PopularListingsView, UserViewsHistoryView

urlpatterns = [
    path("view/", RegisterViewView.as_view()),
    path("popular/", PopularListingsView.as_view()),
    path("my/", UserViewsHistoryView.as_view()),
]
