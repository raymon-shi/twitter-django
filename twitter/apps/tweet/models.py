from django.db import models
from twitter.apps.account.models import Profile


class Tweet(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False)
    body = models.TextField(null=False, blank=False)
    author_profile_url = models.URLField(null=True, blank=True)
    num_of_comments = models.PositiveIntegerField(default=0)
    num_of_retweets = models.PositiveIntegerField(default=0)
    num_of_likes = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ['-created']

    def __str__(self):
        return self.body


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent_tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="p_tweet")
    curr_tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="c_tweet")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class Retweet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=50)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
