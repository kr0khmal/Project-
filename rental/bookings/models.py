from django.db import models
from django.conf import settings
from listings.models import Listing


class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("canceled", "Canceled"),
    )

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.tenant.email} ({self.status})"
