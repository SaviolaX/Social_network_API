from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .serializers import (PostSerializer, PostDetailSerializer)
from ..models import Post
from analitics.models import LikesActivity
from users.api.api_view import check_jwt_existing_or_logout


class LikePost(APIView):
    """Like post"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Add user to post's list of likes
        and create like action"""
        try:
            check_jwt_existing_or_logout(request)
            user = User.objects.get(id=request.user.id)
            post = Post.objects.get(id=id)
            if user in post.likes.all():
                return Response('You have liked it alreary',
                                status=status.HTTP_403_FORBIDDEN)
            else:
                post.likes.add(user)
                LikesActivity.objects.get_or_create(
                    user=user, post=post)
                return Response('You liked the post',
                                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response('You are not logged in.')


class UnlikePost(APIView):
    """Unlike post"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Remove user from post's list of likes
        and delete like action"""
        try:
            check_jwt_existing_or_logout(request)
            user = User.objects.get(id=request.user.id)
            post = Post.objects.get(id=id)
            if user in post.likes.all():
                post.likes.remove(user)
                try:
                    remove_like_action = LikesActivity.objects.get(
                        user=user, post=post)
                    remove_like_action.delete()
                except LikesActivity.DoesNotExist:
                    pass
                return Response('You unliked the post',
                                status=status.HTTP_200_OK)
            else:
                return Response('You unliked it alreary',
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response('You are not logged in.')


class PostsList(APIView):
    """Get a list of all posts"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_jwt_existing_or_logout(request)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetail(generics.RetrieveUpdateAPIView):
    """Get post and edit"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, id):
        """Edit post"""
        check_jwt_existing_or_logout(request)
        post = Post.objects.get(id=id)
        if request.user.id == post.author.id:
            serializer = PostDetailSerializer(instance=post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response('Something went wrong',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You can not edit profile',
                            status=status.HTTP_403_FORBIDDEN)


class CreatePost(generics.CreateAPIView):
    """Creates post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
