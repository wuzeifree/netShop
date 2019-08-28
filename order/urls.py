#coding=utf-8

from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.ToOrderView.as_view()),
    re_path(r'^order.html$', views.OrderList.as_view()),
    re_path(r'^topay/', views.ToPayView.as_view()),
    re_path(r'^checkPay/', views.CheckPayView.as_view()),

]