from rest_framework.views import APIView
from rest_framework.response import Response

from seats.models import Seat
from reservations.models import Reservation, ReservationStatus
from showtimes.models import Showtime
from django.utils import timezone

class SeatListAPIView(APIView):

    def get(self, request, showtime_id):

        showtime = Showtime.objects.get(id=showtime_id)

        seats = Seat.objects.filter(
            venue=showtime.venue
        ).order_by("row", "seat_number")

        result = []

        for seat in seats:

            reservation = Reservation.objects.filter(
                seat=seat,
                showtime=showtime
            ).first()

            status = "AVAILABLE"

            if reservation:

                if (
                    reservation.status == ReservationStatus.HELD
                    and reservation.hold_expiry < timezone.now()
                ):
                    reservation.delete()

                else:
                    status = reservation.status

            result.append({
                "seat_id": seat.id,
                "row": seat.row,
                "seat_number": seat.seat_number,
                "status": status
            })

        return Response(result)


class BookingSummaryAPIView(APIView):

    def get(self, request, showtime_id):

        showtime = Showtime.objects.get(id=showtime_id)

        total_seats = Seat.objects.filter(
            venue=showtime.venue
        ).count()

        booked = Reservation.objects.filter(
            showtime=showtime,
            status=ReservationStatus.BOOKED
        ).count()

        held = Reservation.objects.filter(
            showtime=showtime,
            status=ReservationStatus.HELD,
            hold_expiry__gt=timezone.now()
        ).count()

        available = total_seats - booked - held

        return Response(
            {
                "total_seats": total_seats,
                "booked": booked,
                "held": held,
                "available": available
            }
        )