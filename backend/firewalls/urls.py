from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.firewall_list_view, name='firewall-list'),
    path('<str:pk>/', views.firewall_detail_view, name='firewall-detail'),
]