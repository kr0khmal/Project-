from django.urls import path
from .views import SaveSearchQueryView, PopularSearchesView, UserSearchHistoryView

urlpatterns = [
    path("save/", SaveSearchQueryView.as_view()),
    path("popular/", PopularSearchesView.as_view()),
    path("my/", UserSearchHistoryView.as_view()),
]
