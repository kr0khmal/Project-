from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from .models import SearchQuery
from .serializers import SearchQuerySerializer
from django.db import models


class SaveSearchQueryView(APIView):
    """
    POST: {"query": "Berlin 2 rooms"}
    Сохраняет поисковый запрос
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response({"error": "query is required"}, status=400)

        user = request.user if request.user.is_authenticated else None

        obj, created = SearchQuery.objects.get_or_create(
            user=user,
            query=query
        )

        if not created:
            obj.count += 1
            obj.save()

        return Response({"status": "saved", "query": query})
    

class PopularQueriesView(APIView):
    """
    GET: выводит запросы, отсортированные по популярности
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queries = SearchQuery.objects.values("query").annotate(
            total=models.Sum("count")
        ).order_by("-total")

        return Response(list(queries))


class UserSearchHistoryView(generics.ListAPIView):
    """
    GET: история поиска пользователя
    """
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchQuery.objects.filter(
            user=self.request.user
        ).order_by("-last_searched")
