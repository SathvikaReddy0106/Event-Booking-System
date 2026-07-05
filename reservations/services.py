from datetime import timedelta

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from reservations.models import Reservation, ReservationStatus
from seats.models import Seat
from showtimes.models import Showtime


class ReservationService:

    @staticmethod
    @transaction.atomic
    def hold_seat(user_id, showtime_id, seat_id):

        user = User.objects.get(id=user_id)

        showtime = Showtime.objects.get(id=showtime_id)

        seat = Seat.objects.select_for_update().get(id=seat_id)

        existing = Reservation.objects.filter(
            seat=seat,
            showtime=showtime
        ).first()

        if existing:

            if (
                existing.status == ReservationStatus.HELD
                and existing.hold_expiry < timezone.now()
            ):
                existing.delete()

            else:
                raise ValueError("Seat is already held or booked.")

        reservation = Reservation.objects.create(
            user=user,
            seat=seat,
            showtime=showtime,
            status=ReservationStatus.HELD,
            hold_expiry=timezone.now() + timedelta(minutes=2),
        )

        return reservation
    
    @staticmethod
    @transaction.atomic
    def confirm_reservation(user_id, reservation_id):

        reservation = Reservation.objects.select_for_update().filter(
            id=reservation_id
        ).first()

        if reservation is None:
            raise ValueError("Reservation does not exist.")

        if reservation.user_id != user_id:
            raise ValueError("This reservation does not belong to you.")

        if reservation.status == ReservationStatus.BOOKED:
            return reservation

        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError("Reservation has already been cancelled.")

        if (
            reservation.status == ReservationStatus.HELD
            and reservation.hold_expiry < timezone.now()
        ):
            reservation.delete()
            raise ValueError("Hold has expired.")

        reservation.status = ReservationStatus.BOOKED
        reservation.confirmed_at = timezone.now()
        reservation.save()

        return reservation
    @staticmethod
    @transaction.atomic
    def cancel_reservation(user_id, reservation_id):

        reservation = Reservation.objects.select_for_update().filter(
            id=reservation_id
        ).first()

        if reservation is None:
            raise ValueError("Reservation does not exist.")

        if reservation.user_id != user_id:
            raise ValueError("This reservation does not belong to you.")

        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError("Reservation already cancelled.")

        reservation.status = ReservationStatus.CANCELLED
        reservation.save()

        return reservation