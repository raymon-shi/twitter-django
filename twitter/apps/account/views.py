from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from twitter.apps.tweet.models import Tweet, Retweet, Hashtag
from django.contrib.auth.models import User
from django.db.models import Q


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        body = request.POST.get('tweet-body')
        profile = Profile.objects.get(user=request.user)
        tweet = Tweet.objects.create(author=profile, body=body)

        profile.num_of_tweets = (
            Tweet.objects
            .filter(author=profile)
            .count()
        )

        split_tweet = body.split(' ')
        for word in split_tweet:
            if word[0] == '#':
                hashtag = Hashtag.objects.create(hashtag=word, tweet=tweet)
                hashtag.save()

        tweet.save()
        profile.save()

    followers = (
        Follow.objects
        .filter(follower=request.user.profile)
        .values_list('followee')
    )
    retweets = (
        Retweet.objects
        .filter(user=request.user.profile)
        .values_list('tweet')
    )
    tweets = (
        Tweet.objects
        .filter(
            Q(author_id__in=followers) |
            Q(author=request.user.profile) |
            Q(id__in=retweets)
        )
        .order_by('-created'))
    profiles = Profile.objects.all()

    return render(request, 'account/home.html', {'tweets': tweets, 'retweets': retweets, 'profiles': profiles})


@login_required(login_url='login')
def logout_(request):
    logout(request)

    return redirect('splash')


@login_required(login_url='login')
def profile(request, id):
    if request.method == 'GET':
        page = 'profile'
        profile: Profile = Profile.objects.get(id=id)

        retweets = (
            Retweet.objects
            .filter(user=profile)
            .values_list('tweet')
        )
        tweets = (
            Tweet.objects
            .filter(
                Q(author=profile) |
                Q(id__in=retweets)
            )
            .order_by('-created')
        )

        connection = (
            Follow.objects
            .filter(
                followee=profile,
                follower=request.user.profile
            )
            .exists()
        )

        profiles = Profile.objects.all()

        return render(request, 'account/profile.html', {'tweets': tweets, 'profile': profile, 'page': page, 'connection': connection, 'profiles': profiles})


@login_required(login_url='login')
def updateProfile(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        handle = request.POST.get('handle')
        description = request.POST.get('description')
        birthday = request.POST.get('birthday')
        profile_url = request.POST.get('profile')
        personal_url = request.POST.get('personal')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        profile.handle = handle
        profile.description = description
        profile.birthday = birthday
        profile.profile_url = profile_url
        profile.personal_url = personal_url

        user.save()
        profile.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def searchProfile(request):
    if request.method == "GET":
        search = request.GET.get('search')
        profiles = (
            Profile.objects
            .filter(
                Q(handle__icontains=search)
            )
        )

        return render(request, 'account/search.html', {'profiles': profiles})


@login_required(login_url='login')
def follow(request, id):
    if request.method == "GET":
        followee = Profile.objects.get(id=id)
        follower = request.user.profile

        connection = Follow.objects.filter(
            followee=followee, follower=follower)

        if (connection.exists()):
            connection.delete()
        else:
            Follow.objects.create(followee=followee, follower=follower)

        followee.num_of_followers = (
            Follow.objects
            .filter(
                followee=followee)
            .count()
        )
        follower.num_of_followings = (
            Follow.objects
            .filter(
                follower=follower)
            .count()
        )

        followee.save()
        follower.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def viewFollowers(request, id):
    profile = Profile.objects.get(id=id)
    follows = Follow.objects.filter(followee=profile)
    return render(request, 'account/followers.html', {'profile': profile, 'follows': follows})


@login_required(login_url='login')
def viewFollowings(request, id):
    profile = Profile.objects.get(id=id)
    follows = Follow.objects.filter(
        follower=profile)
    return render(request, 'account/followings.html', {'profile': profile, 'follows': follows})
