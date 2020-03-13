from django.conf.urls import url, include

from .views import UserView

urlpatterns = [
    url(r'^(.*?)/$', UserView.as_view()),
]