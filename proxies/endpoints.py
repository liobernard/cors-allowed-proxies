from django.urls import re_path

from .api import HomeAPI, ProxiesAPI, CSVAPI, TestedAPI

urlpatterns = [
    re_path(r'^$', HomeAPI.as_view()),
    re_path(r'^proxies/$', ProxiesAPI.as_view()),
    re_path(r'^proxies/csv/$', CSVAPI.as_view()),
    re_path(r'^proxy/$', TestedAPI.as_view()),
]
