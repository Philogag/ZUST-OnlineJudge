from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/submition/', include("submition.urls")),
    url(r'^api/problem/', include('problem.urls')),
    url(r'^api/user/', include('user.urls')),
    
]
