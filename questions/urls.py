from django.urls import path
from questions.views import question_page

urlpatterns = [
    path("", question_page, name="question"),
]
