from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework import status

import jwt
import datetime

from .serializers import UserSerializer
from ..models import User
from analitics.models import UserLoginActivity


def check_jwt_existing_or_logout(request):
    """Check if jwt token exists, allowed access to app,
    if jwt token doesn't exist --> logout"""
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        logout(request)
        return redirect('login_user')


class UserByIdView(APIView):
    """Get user view"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Display user's page"""
        check_jwt_existing_or_logout(request)
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User does not exist.",
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """Edit user's page"""
        check_jwt_existing_or_logout(request)
        user = User.objects.get(id=id)
        if request.user == user:
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('You made a mistake in sintaksis',
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('You can not edit the user info',
                            status=status.HTTP_403_FORBIDDEN)


class RegisterView(APIView):
    """User registration view"""

    def post(self, request):
        """If POST, creates user"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """User log in view"""

    def post(self, request):
        """checks user's data
        if user's data in db, log in user"""
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        login(request, user=user)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response()

        # create coockie
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token,
        }

        UserLoginActivity.objects.create(user=user)

        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired!')

        user = User.objects.get(id=payload['id'])

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": 'success'
        }
        logout(request)

        return response
