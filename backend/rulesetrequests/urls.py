from django.urls import path

from . import views

urlpatterns = [
    path('', views.rulesetrequest_list_create_view, name='rulesetrequest-list'),
    #path('<int:pk>/update/', views.rulesetrequest_update_view, name='rulesetrequest-edit'),
    path('<int:pk>/approve/', views.rulesetrequest_status_update_view, name='rulesetrequest-approve'),
    path('<int:pk>/refuse/', views.rulesetrequest_status_update_view, name='rulesetrequest-refuse'),
    path('<int:pk>/', views.rulesetrequest_detail_view, name='rulesetrequest-detail'),
]