from rest_framework.views import APIView
from rest_framework.response import Response

class SeatListAPIView(APIView):

    def get(self, request, showtime_id):
        pass