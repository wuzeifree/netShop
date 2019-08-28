from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^register/', views.RegisterView.as_view()),
    re_path(r'^checkUname/', views.CheckUnameView.as_view()),
    re_path(r'^center/', views.CenterView.as_view()),
    re_path(r'^logout/', views.LoginOut.as_view()),
    re_path(r'^login/', views.Login.as_view()),
    re_path(r'^loadCode.jpg', views.LoadCode.as_view()),
    re_path(r'^checkcode/', views.CheckCode.as_view()),
    re_path(r'^address/', views.AddressView.as_view()),
    re_path(r'^loadArea/', views.LoadAreaView.as_view()),
]