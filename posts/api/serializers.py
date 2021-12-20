from rest_framework import serializers

from users.models import User
from ..models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'entry',
                  'likes', 'total_likes', 'datetime')

    def get_total_likes(self, instance):
        return instance.likes.count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'entry', 'datetime')
