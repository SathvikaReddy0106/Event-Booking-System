from rest_framework import serializers


class SeatStatusSerializer(serializers.Serializer):
    seat_id = serializers.IntegerField()
    row = serializers.CharField()
    seat_number = serializers.IntegerField()
    status = serializers.CharField()