from django.db import models
from django.conf import settings


class SearchQuery(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_queries",
        null=True,
        blank=True
    )
    keyword = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "keyword")

    def __str__(self):
        return f"{self.keyword} ({self.count})"
