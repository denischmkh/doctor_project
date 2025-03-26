from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_profile/<int:id>/', views.doctor_profile, name='doctor_profile'),
    path('doctors/<int:page>/', views.doctor_list, name='doctor_list_paginator'),
    path('select_specializations', views.select_specializations, name='select_specializations'),
    path('select_gender', views.select_gender, name='select_genders'),
    path('select_languages', views.select_languages, name='select_languages'),
]