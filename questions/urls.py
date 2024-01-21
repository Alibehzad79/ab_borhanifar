from django.urls import path
from questions.views import question_page
from accounts.views import go_to_gateway_view, callback_gateway_view

app_name = "question_app"
urlpatterns = [
    path("", question_page, name="question"),
    path('callback-gateway/', callback_gateway_view, name="callback-gateway"),
    path('go-to-gateway-view/', go_to_gateway_view, name="go-to-gateway-view"),
]
