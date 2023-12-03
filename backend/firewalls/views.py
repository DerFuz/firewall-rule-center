from rest_framework import generics

from .models import FirewallObject
from .serializers import FirewallObjectSerializer
from api.mixins import RulePermissionMixin

class FirewallListAPIView(
    RulePermissionMixin,
    generics.ListAPIView):
    queryset = FirewallObject.objects
    serializer_class = FirewallObjectSerializer
    

firewall_list_view = FirewallListAPIView.as_view()


class FirewallDetailAPIView(
    RulePermissionMixin,
    generics.RetrieveAPIView):
    queryset = FirewallObject.objects
    serializer_class = FirewallObjectSerializer
    lookup_field = 'pk'

firewall_detail_view = FirewallDetailAPIView.as_view()