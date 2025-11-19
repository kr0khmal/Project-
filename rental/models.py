from django.db import models
from django.conf import settings
from listings.models import Listing


class ListingView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="views"
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed {self.listing}"
