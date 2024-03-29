# users/urls.py
from django.urls import path
from . import views
from users.updatefucs import  GetUserDetails
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('usersview/', views.UserListView.as_view()),
    path('current/', GetUserDetails.as_view()),
    path('profile_data/', views.user_profile.as_view()),
    path('change_password/', views.User_password_change.as_view()),
    path('plan/', views.plan_update.as_view()),
    path('usocial/',views.usocialogin)
]
