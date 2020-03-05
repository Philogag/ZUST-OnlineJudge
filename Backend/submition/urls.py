from django.conf.urls import url, include

from .views import SubmitionView, SubmitionALLView, JudgeAPI, AdminAPI

urlpatterns = [
    url(r'^all/', SubmitionALLView.as_view()),
    url(r'^(\d+)/', SubmitionView.as_view()),
    url(r'^new/', SubmitionView.as_view()),
    url(r'^admin/', AdminAPI.as_view()),
    url(r'^judge/', JudgeAPI.as_view()),
]