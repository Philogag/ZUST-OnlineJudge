from django.conf.urls import url, include

from .views import SubmissionView, SubmissionALLView, JudgeAPI, AdminAPI

urlpatterns = [
    url(r'^all/', SubmissionALLView.as_view()),
    url(r'^(\d+)/', SubmissionView.as_view()),
    url(r'^new/', SubmissionView.as_view()),
    url(r'^admin/$', AdminAPI.as_view()),
    url(r'^judger/', JudgeAPI.as_view()),
]