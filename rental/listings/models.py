from django.db import models
from django.conf import settings


class Listing(models.Model):
    HOUSING_TYPES = (
        ("apartment", "Apartment"),
        ("house", "House"),
        ("studio", "Studio"),
        ("room", "Room"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    rooms = models.IntegerField()
    housing_type = models.CharField(max_length=50, choices=HOUSING_TYPES)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    views_count = models.IntegerField(default=0)  # для сортировки по популярности

    def __str__(self):
        return f"{self.title} ({self.price}€)"


class ListingView(models.Model):
    """
    История просмотров объявлений
    """

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]
