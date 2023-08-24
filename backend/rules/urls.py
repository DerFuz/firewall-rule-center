from django.urls import path

from . import views

urlpatterns = [
    path('', views.rule_list_create_view, name='rule-list'),
    path('<int:pk>/update/', views.rule_update_view, name='rule-edit'),
    path('<int:pk>/delete/', views.rule_delete_view),
    path('<int:pk>/', views.rule_detail_view, name='rule-detail'),
]