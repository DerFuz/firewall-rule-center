from rest_framework import generics
from django.contrib.auth import get_user_model
from api.mixins import UserPermissionMixin
from api.serializers import UserPublicSerializer

class UserListAPIView(
    UserPermissionMixin,
    generics.ListAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserPublicSerializer
    
user_list_view = UserListAPIView.as_view()