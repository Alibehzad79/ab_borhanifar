from django.urls import path
from accounts.views import login_page, logout_page, register_page, profile, change_password, user_downloads, \
    user_questions

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_page, name="logout"),
    path("profile/", profile, name="profile"),
    path("change-password/", change_password, name="change_password"),
    path("downloads/", user_downloads, name="downloads"),
    path("downloads/", user_downloads, name="downloads"),
    path("questions/", user_questions, name="user_questions"),
]
