from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import (LikesActivitySerializer,
                          LikesLogActivitySerializer, UserLoginSerializer)
from users.models import User
from ..models import LikesActivity, UserLoginActivity
from users.api.api_view import check_jwt_existing_or_logout


class UserLoginLogs(APIView):
    """Get user's last login log"""

    def get(self, request, id):
        check_jwt_existing_or_logout(request)
        user = User.objects.get(id=id)
        logs = UserLoginActivity.objects.filter(
            user=user).order_by("-login").first()
        serializer = UserLoginSerializer(logs)
        return Response(serializer.data)


class LikesActivityList(generics.ListAPIView):
    """Display all likes activity"""
    queryset = LikesActivity.objects.all()
    serializer_class = LikesActivitySerializer


class LikesActivityRangeFilter(APIView):
    """Display likes activity for chosen period"""

    def get(self, request, from_year, from_month, from_day,
            to_year, to_month, to_day):
        """Get dates from user, filter and group likes by date"""
        check_jwt_existing_or_logout(request)

        from_date = f"{from_year}-{from_month}-{from_day}"
        to_date = f"{to_year}-{to_month}-{to_day}"

        likes = LikesActivity.objects.filter(
            created__range=[from_date, to_date]).order_by(
            'created').distinct('created').only('created')

        serializer = LikesLogActivitySerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
