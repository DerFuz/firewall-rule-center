from django.urls import path, include

from .views import api_home

urlpatterns = [
    path('', api_home),
    path('rules/', include('rules.urls')),
]