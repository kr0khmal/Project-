from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SearchQuery
from .serializers import SearchQuerySerializer


class SaveSearchQueryView(APIView):
    """
    POST: {"keyword": "Berlin"}
    сохраняет запрос для пользователя
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        keyword = request.data.get("keyword", "").strip().lower()

        if not keyword:
            return Response({"error": "Keyword is required."}, status=400)

        user = request.user if request.user.is_authenticated else None

        obj, created = SearchQuery.objects.get_or_create(
            user=user,
            keyword=keyword
        )

        if not created:
            obj.count += 1
            obj.save()

        return Response({"status": "saved", "keyword": keyword})
    

class PopularSearchesView(generics.ListAPIView):
    """
    GET: список популярных запросов
    """
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SearchQuery.objects.order_by("-count")[:50]


class UserSearchHistoryView(generics.ListAPIView):
    """
    GET: история поиска пользователя
    """
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchQuery.objects.filter(user=self.request.user).order_by("-last_used")
