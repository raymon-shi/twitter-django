from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet, Like, Comment, Retweet, Hashtag
from twitter.apps.account.models import Profile


@login_required(login_url='login')
def allTweets(request):
    if request.method == "GET":
        tweets = (
            Tweet.objects
            .all()
            .order_by('-created')
        )
        profiles = Profile.objects.all()

    return render(request, 'tweet/all.html', {'tweets': tweets, 'profiles': profiles})


@login_required(login_url='login')
def viewTweet(request, id):
    try:
        tweet = Tweet.objects.get(id=id)
    except:
        return redirect('home')

    if request.method == "POST":
        body = request.POST.get('tweet-body')
        profile = Profile.objects.get(user=request.user)
        new_tweet = Tweet.objects.create(author=profile, body=body)

        profile.num_of_tweets = (
            Tweet.objects
            .filter(author=profile)
            .count()
        )

        new_tweet.save()
        profile.save()

        comment = Comment.objects.create(
            author=profile,
            parent_tweet=tweet,
            curr_tweet=new_tweet,
            body=body)

        comment.save()

        tweet.num_of_comments = (
            Comment.objects
            .filter(parent_tweet=tweet)
            .count()
        )

        tweet.save()

        return redirect(request.META.get('HTTP_REFERER'))

    comments = (
        Comment.objects
        .filter(parent_tweet=tweet)
        .order_by('-created')
    )
    profiles = Profile.objects.all()

    return render(request, 'tweet/tweet_standalone.html', {'tweet': tweet, 'comments': comments, 'profiles': profiles})


@login_required(login_url='login')
def deleteTweet(request, id):
    tweet = Tweet.objects.get(id=id)
    parent_tweet = None
    if request.method == 'GET':
        profile = tweet.author
        comment = (
            Comment.objects
            .filter(curr_tweet=tweet)
            .first()
        )
        tweet.delete()

        if comment:
            parent_tweet = comment.parent_tweet
        if parent_tweet:
            parent_tweet.num_of_comments = (
                Comment.objects
                .filter(parent_tweet=parent_tweet)
                .count()
            )
            parent_tweet.save()

        profile.num_of_tweets = (
            Tweet.objects
            .filter(author=profile)
            .count()
        )
        profile.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def likeTweet(request, id):
    if request.method == 'GET':
        tweet = Tweet.objects.get(id=id)
        profile = request.user.profile
        like = Like.objects.filter(user=profile, tweet=tweet)

        if like.exists():
            like.delete()
        else:
            Like.objects.create(user=profile, tweet=tweet)

        tweet.num_of_likes = (
            Like.objects
            .filter(tweet=tweet)
            .count()
        )
        tweet.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def retweet(request, id):
    if request.method == "GET":
        tweet = Tweet.objects.get(id=id)
        retweet = Retweet.objects.filter(
            user=request.user.profile,
            tweet=tweet
        )

        if (retweet.exists()):
            retweet.delete()
        else:
            retweet = Retweet.objects.create(
                user=request.user.profile,
                tweet=tweet
            )

        retweet_count = (
            Retweet.objects
            .filter(tweet=tweet)
            .count()
        )
        tweet.num_of_retweets = retweet_count
        tweet.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def viewHashtag(request, hashtag):
    if request.method == "GET":
        hashtags = Hashtag.objects.filter(
            hashtag=hashtag)
        hashtag_name = hashtags.first().hashtag
    profiles = Profile.objects.all()

    return render(request, 'tweet/hashtag.html', {'hashtags': hashtags, 'hashtag_name': hashtag_name, 'profiles': profiles})
