from django.urls import path
from .views import home, logout_, profile, updateProfile, searchProfile, follow, viewFollowers, viewFollowings

urlpatterns = [
    path('home/', home, name='home'),
    path('logout/', logout_, name='logout'),
    path(f'search-profile/', searchProfile, name='search_profile'),
    path('profile/<str:id>', profile, name='profile'),
    path('update-profile/<str:id>', updateProfile, name='update_profile'),

    path('follow/<str:id>', follow, name='follow'),
    path('followers/<str:id>', viewFollowers, name="view_followers"),
    path('followings/<str:id>', viewFollowings, name="view_followings"),

]
