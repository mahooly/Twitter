from django.contrib.auth.models import User
from django.db import models
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='../media/profile_pics/', default='../media/profile_pics/no-picture.png')
    bio = models.TextField(max_length=100, default=None, null=True)
    joined = models.DateField(auto_now_add=True)
    birthday = models.DateField(default=None, null=True)
    authentication_key = models.UUIDField(unique=True, default=uuid.uuid4)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')


class RequestData(models.Model):
    ip = models.GenericIPAddressField()
    browser = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    authorized = models.BooleanField(default=True)


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
