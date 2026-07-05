from rest_framework import serializers


class HoldSeatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    showtime_id = serializers.IntegerField(min_value=1)
    seat_id = serializers.IntegerField(min_value=1)


class ConfirmReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)


class CancelReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)