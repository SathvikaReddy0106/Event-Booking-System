from django.db import models
from venues.models import Venue


class Showtime(models.Model):
    """
    Represents a movie show scheduled at a venue.
    """

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="showtimes"
    )

    movie_name = models.CharField(max_length=150)

    start_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "showtimes"
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.movie_name} - {self.start_time}"