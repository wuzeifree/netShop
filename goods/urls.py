#coding=utf-8
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view()),
    re_path(r'^category/(\d+)$', views.IndexView.as_view()),
    re_path(r'^category/(\d+)/page/(\d+)$', views.IndexView.as_view()),
    re_path(r'^goodsdetails/(\d+)$', views.GoodsDetailView.as_view()),
]