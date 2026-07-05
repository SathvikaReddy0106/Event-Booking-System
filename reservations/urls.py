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
        "seat/hold/",
        HoldSeatAPIView.as_view(),
        name="hold-seat",
    ),

    path(
        "booking/confirm/",
        ConfirmReservationAPIView.as_view(),
        name="confirm",
    ),

    path(
        "booking/cancel/",
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