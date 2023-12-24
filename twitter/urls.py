from django.contrib import admin
from django.urls import path, include
from .views import splash

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash, name='splash'),
    path('', include('twitter.apps.signup.urls')),
    path('', include('twitter.apps.account.urls')),
    path('', include('twitter.apps.tweet.urls')),
]
