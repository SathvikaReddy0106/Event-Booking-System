from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HoldSeatSerializer, ConfirmReservationSerializer, CancelReservationSerializer
from .services import ReservationService

from seats.models import Seat
from reservations.models import Reservation, ReservationStatus
from showtimes.models import Showtime
from django.utils import timezone


class HoldSeatAPIView(APIView):

    def post(self, request):

        serializer = HoldSeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reservation = ReservationService.hold_seat(
                serializer.validated_data["user_id"],
                serializer.validated_data["showtime_id"],
                serializer.validated_data["seat_id"],
            )

            return Response(
                {
                    "reservation_id": reservation.id,
                    "status": reservation.status,
                    "hold_expiry": reservation.hold_expiry,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_409_CONFLICT,
            )


class ConfirmReservationAPIView(APIView):

    def post(self, request):

        serializer = ConfirmReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reservation = ReservationService.confirm_reservation(
                serializer.validated_data["user_id"],
                serializer.validated_data["reservation_id"],
            )

            return Response(
                {
                    "reservation_id": reservation.id,
                    "status": reservation.status,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_409_CONFLICT,
            )


class CancelReservationAPIView(APIView):

    def delete(self, request):

        serializer = CancelReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            reservation = ReservationService.cancel_reservation(
                serializer.validated_data["user_id"],
                serializer.validated_data["reservation_id"],
            )

            return Response(
                {
                    "reservation_id": reservation.id,
                    "status": reservation.status,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_409_CONFLICT,
            )


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