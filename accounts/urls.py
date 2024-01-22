from django.urls import path
from accounts.views import login_page, logout_page, register_page, profile, change_password, user_downloads, \
    user_questions, user_questions_complete, recovery_password, send_email_done, set_recovery_password

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_page, name="logout"),
    path("profile/", profile, name="profile"),
    path("change-password/", change_password, name="change_password"),
    path("recovery-password/", recovery_password, name="recover_password"),
    path("recovery-password/send-email-done/", send_email_done, name="send_email_done"),
    path("recovery-password/set-password/", set_recovery_password, name="set-recover-password"),
    path("downloads/", user_downloads, name="downloads"),
    path("downloads/", user_downloads, name="downloads"),
    path("questions/", user_questions, name="user_questions"),
    path("questions-complete/", user_questions_complete, name="questions-complete"),
]
