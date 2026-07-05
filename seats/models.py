from django.db import models
from venues.models import Venue


class Seat(models.Model):
    """
    Represents a seat inside a venue.
    """

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="seats"
    )

    row = models.CharField(max_length=5)

    seat_number = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "seats"

        ordering = ["row", "seat_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["venue", "row", "seat_number"],
                name="unique_seat_per_venue"
            )
        ]

    def __str__(self):
        return f"{self.venue.name} - {self.row}{self.seat_number}"