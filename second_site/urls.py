from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/<str:specialisation>/<int:page>/', views.get_doctors_by_specialisation, name='get_doctors_by_specialisation'),
]