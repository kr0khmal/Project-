from django.urls import path
from .views import SaveSearchQueryView, PopularQueriesView, UserSearchHistoryView

urlpatterns = [
    path("save/", SaveSearchQueryView.as_view()),
    path("popular/", PopularQueriesView.as_view()),
    path("my/", UserSearchHistoryView.as_view()),
]
