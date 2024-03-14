from django.urls import re_path as url

from highobjects.views import DataView

urlpatterns = [
    url('gkpw',DataView.as_view()),
]