from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.rule_list_create_view, name='rule-list'),
    path('<int:pk>/update/', views.rule_update_view, name='rule-edit'),
    path('<int:pk>/delete/', views.rule_delete_view, name='rule-delete'),
    path('<int:pk>/', views.rule_detail_view, name='rule-detail'),
    path('requests/', include('rulesetrequests.urls'))
]