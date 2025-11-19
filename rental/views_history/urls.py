from django.urls import path
from .views import SaveViewRecordView, PopularListingsView, UserViewHistoryView

urlpatterns = [
    path("save/", SaveViewRecordView.as_view()),
    path("popular/", PopularListingsView.as_view()),
    path("my/", UserViewHistoryView.as_view()),
]
path("api/views/", include("views_history.urls")),
