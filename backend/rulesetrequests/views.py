from rest_framework import generics

from .models import RuleSetRequest
from .serializers import RuleSetRequestSerializer

class RuleSetRequestListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer

    def perform_create(self, serializer):
        data = {
            'created_by': self.request.user,
            'last_updated_by': self.request.user
        }
        serializer.save(**data)


rulesetrequest_list_create_view = RuleSetRequestListCreateAPIView.as_view()


class RuleSetRequestDetailAPIView(
    generics.RetrieveAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer
    lookup_field = "pk"

rulesetrequest_detail_view = RuleSetRequestDetailAPIView.as_view()


class RuleSetRequestUpdateAPIView(
    generics.UpdateAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        data = {
            'last_updated_by': self.request.user
        }
        instance = serializer.save(**data)

rulesetrequest_update_view = RuleSetRequestUpdateAPIView.as_view()