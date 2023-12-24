from django.urls import path
from .views import allTweets, deleteTweet, likeTweet, viewTweet, retweet, viewHashtag

urlpatterns = [
    path('all/', allTweets, name='all_tweets'),
    path('tweet/<str:id>', viewTweet, name='view_tweet'),
    path('delete-tweet/<str:id>', deleteTweet, name='delete_tweet'),
    path('like-tweet/<str:id>', likeTweet, name='like_tweet'),
    path('retweet/<str:id>', retweet, name="retweet"),
    path('hashtag/<str:hashtag>', viewHashtag, name="view_hashtag"),
]
