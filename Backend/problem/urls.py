from django.conf.urls import url, include

from .views import ProblemAllView, ProblemView

urlpatterns = [
    url(r'^all/', ProblemAllView.as_view()),
    url(r'(\d+)/', ProblemView.as_view()),
    url(r'^new/', ProblemView.as_view()),
]
