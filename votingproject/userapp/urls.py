from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout, name='logout'),
    path('', BaseProfileView.as_view(), name='userprofile'),
    path('profilepage/', ProfilePage.as_view(), name='profilepage'),
    path('updateprofile/', UserProfileUpdateView.as_view(), name='updateprofile'),
    
]


