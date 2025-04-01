from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_profile/<int:id>/', views.doctor_profile, name='doctor_profile'),
    path('doctors/<int:page>/', views.doctor_list, name='doctor_list_paginator'),
    path('select_filters', views.select_filters, name='select_filters'),
    path('pages/clinics/', views.get_clinics, name='get_clinics'),
    path('pages/clinics/<int:page>', views.get_clinics, name='get_clinics'),
]