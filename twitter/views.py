from django.shortcuts import render, redirect


def splash(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'splash.html')
