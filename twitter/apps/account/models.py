from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50, unique=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    birthday = models.DateField(null=True, blank=True)
    profile_url = models.URLField(null=True, blank=True)
    personal_url = models.URLField(null=True, blank=True)
    num_of_followers = models.PositiveIntegerField(default=0)
    num_of_followings = models.PositiveIntegerField(default=0)
    num_of_tweets = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.handle


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower_to")
    followee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followee_by")
