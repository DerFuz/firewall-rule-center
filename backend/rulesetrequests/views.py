from rest_framework import generics, status
from rest_framework.response import Response

from .models import RuleSetRequest
from .serializers import RuleSetRequestSerializer, RuleSetRequestStatusSerializer
from api.mixins import RuleSetRequestPermissionMixin

class RuleSetRequestListCreateAPIView(
    RuleSetRequestPermissionMixin,
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
    RuleSetRequestPermissionMixin,
    generics.RetrieveAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer
    lookup_field = "pk"

rulesetrequest_detail_view = RuleSetRequestDetailAPIView.as_view()

class RuleSetRequestStatusUpdateAPIView(
    RuleSetRequestPermissionMixin,
    generics.RetrieveAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestStatusSerializer
    lookup_field = "pk"
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(type(instance.approver))
        # print(type(request.user))
        # print(f'Instance-Approver: {instance.approver.id}, Request-User: {request.user.id}')
        if instance.approver != request.user:
            return Response("You are not the defined approver", status=status.HTTP_401_UNAUTHORIZED)
        
        path = request.get_full_path()
        if path.endswith('/approve/'):
            print('APR')
        elif path.endswith('/refuse/'):
            print('REF')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

rulesetrequest_status_update_view = RuleSetRequestStatusUpdateAPIView.as_view()


class RuleSetRequestUpdateAPIView(
    RuleSetRequestPermissionMixin,
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