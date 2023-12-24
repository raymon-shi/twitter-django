from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from twitter.apps.account.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        handle = request.POST.get('handle')
        description = request.POST.get('description')
        birthday = request.POST.get('birthday')
        profile_url = request.POST.get('profile')

        if first_name and last_name and username and password and email and handle and birthday:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email,
            )
            profile = Profile.objects.create(
                user=user,
                handle=handle,
                description=description,
                birthday=birthday,
                profile_url=profile_url)

            user.save()
            profile.save()

            login(request, user)

            return redirect('home')

    return render(request, 'signup/signup_form.html', {})


def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Log in information is not correct!')

    return render(request, 'signup/login_form.html', {})
