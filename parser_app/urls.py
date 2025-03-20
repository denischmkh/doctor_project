from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_profile/<int:id>/', views.doctor_profile, name='doctor_profile'),
    path('doctors/<int:page>/', views.doctor_list, name='doctor_list_paginator'),
]