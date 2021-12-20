from rest_framework import serializers

from ..models import LikesActivity, UserLoginActivity
from posts.models import Post
from users.models import User


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserLoginSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)

    class Meta:
        model = UserLoginActivity
        fields = ('user', 'login',)


class PostTitleSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'entry')


class LikesActivitySerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)
    post = PostTitleSerializer(read_only=True)

    class Meta:
        model = LikesActivity
        fields = ['id', 'user', 'post']


class LikesSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)
    post = PostTitleSerializer(read_only=True)

    class Meta:
        model = LikesActivity
        fields = ['user', 'post']


class LikesLogActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = LikesActivity
        fields = ['created', 'activity']

    activity = serializers.SerializerMethodField('get_likes')

    def get_likes(self, obj):
        likes = LikesActivity.objects.filter(created=obj.created)
        likes_serializer = LikesSerializer(likes, many=True)
        return likes_serializer.data
