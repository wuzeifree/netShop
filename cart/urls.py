#coding=utf-8

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.AddCartView.as_view()),
    re_path(r'^queryAll/', views.QueryAllView.as_view())
]