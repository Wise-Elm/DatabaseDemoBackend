
from django.conf import settings
from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=200, unique=True)
    genre = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(
        max_length=100,
        default="USA"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "city"],
                name="unique_venue_name_city"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.city}"


class Event(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        CANCELED = "canceled", "Canceled"
        POSTPONED = "postponed", "Postponed"

    name = models.CharField(max_length=200)

    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="events"
    )

    date_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_events"
    )

    ticket_url = models.URLField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Performance(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    band = models.ForeignKey(
        Band,
        on_delete=models.PROTECT,
        related_name="performances"
    )

    set_time = models.DateTimeField(
        null=True,
        blank=True
    )

    is_headliner = models.BooleanField(
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "band"],
                name="unique_event_band"
            )
        ]

    def __str__(self):
        return f"{self.band} at {self.event}"


class FavoriteBand(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_bands"
    )

    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "band"],
                name="unique_user_band"
            )
        ]

    def __str__(self):
        return f"{self.user} follows {self.band}"
