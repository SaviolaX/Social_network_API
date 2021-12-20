from django.db import models

from users.models import User


class Post(models.Model):
    """Create post"""
    title = models.CharField(max_length=200)
    entry = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post_author')
    likes = models.ManyToManyField(User,
                                   blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ('-datetime',)

    def __str__(self):
        return self.title
