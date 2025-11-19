from django.db import models
from django.conf import settings
from rental.models import Listing


class ViewRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="view_records",
        null=True,
        blank=True
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="views"
    )
    count = models.PositiveIntegerField(default=1)
    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.listing.title} — {self.count} views"
