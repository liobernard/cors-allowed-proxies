from django.conf.urls import re_path, include

from proxies import endpoints

urlpatterns = [
    re_path(r'^', include(endpoints)),
]