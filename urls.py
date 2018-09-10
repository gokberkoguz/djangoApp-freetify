from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # ex: /polls/
    url(r'app3', views.main, name='freetify'),
    url(r'json_demo.txt', views.jsonResponse, name='freetify'),


]