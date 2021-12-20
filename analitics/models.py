from django.db import models

from posts.models import Post
from users.models import User


class LikesActivity(models.Model):
    """Contain all likes created"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} liked by {self.user}, {self.created}"

    class Meta:
        verbose_name = 'Likes activity'
        verbose_name_plural = 'Likes activities'


class UserLoginActivity(models.Model):
    """Contain user's login info"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='Logged_in_user'
    )
    login = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'user login activities'

    def __str__(self):
        return "{} logged in {}".format(self.user, self.login)
