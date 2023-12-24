from django.urls import path
from .views import signup, login_

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_, name='login'),

]
