from django.conf.urls import url, include
from rest_framework import routers

from .views import SubmitionView, SubmitionsView, JudgeAPI, AdminAPI

urlpatterns = [
    url(r'^all/', SubmitionsView.as_view()),
    url(r'^(\d+)/', SubmitionView.as_view()),
    url(r'^new/', SubmitionView.as_view()),
    url(r'^admin/', AdminAPI.as_view()),
    url(r'^judge/', JudgeAPI.as_view()),
]