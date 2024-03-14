from django.urls import re_path as url

from smokes.views import DataView

urlpatterns = [
    url('smoke',DataView.as_view()),
]