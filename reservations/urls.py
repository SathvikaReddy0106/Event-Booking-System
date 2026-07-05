from django.urls import path

from .views import (
    HoldSeatAPIView,
    ConfirmReservationAPIView,
    CancelReservationAPIView,
    SeatListAPIView,
    BookingSummaryAPIView,
)

urlpatterns = [

    path(
        "hold/",
        HoldSeatAPIView.as_view(),
        name="hold-seat",
    ),

    path(
        "confirm/",
        ConfirmReservationAPIView.as_view(),
        name="confirm",
    ),

    path(
        "cancel/",
        CancelReservationAPIView.as_view(),
        name="cancel",
    ),

    path(
        "showtimes/<int:showtime_id>/seats/",
        SeatListAPIView.as_view(),
        name="seat-list",
    ),

    path(
        "showtimes/<int:showtime_id>/summary/",
        BookingSummaryAPIView.as_view(),
        name="booking-summary",
    ),

]