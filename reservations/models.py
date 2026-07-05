from django.db import models
from django.contrib.auth.models import User
from seats.models import Seat
from showtimes.models import Showtime


class ReservationStatus(models.TextChoices):
    HELD = "HELD", "Held"
    BOOKED = "BOOKED", "Booked"
    CANCELLED = "CANCELLED", "Cancelled"


class Reservation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.HELD
    )

    hold_expiry = models.DateTimeField(
        null=True,
        blank=True
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "reservations"

        ordering = ["-created_at"]

        constraints = [

            models.UniqueConstraint(
                fields=["seat", "showtime"],
                name="unique_seat_showtime"
            )

        ]

        indexes = [

            models.Index(fields=["showtime"]),

            models.Index(fields=["status"]),

            models.Index(fields=["user"]),

        ]

    def __str__(self):
        return f"{self.user.username} - {self.seat} - {self.status}"