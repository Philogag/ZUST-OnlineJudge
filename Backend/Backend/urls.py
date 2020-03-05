from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^api/submition/', include("submition.urls"))
]
