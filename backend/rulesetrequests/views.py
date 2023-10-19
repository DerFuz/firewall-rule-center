from rest_framework import generics, status
from rest_framework.response import Response

from .models import RuleSetRequest
from rules.models import Rule
from rules.serializers import RuleSerializer
from .serializers import RuleSetRequestSerializer
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
        # does not check if status is given - serializer defines it as read-only - value will be overwritten by model default
        serializer.save(**data)

rulesetrequest_list_create_view = RuleSetRequestListCreateAPIView.as_view()


class RuleSetRequestDetailAPIView(
    RuleSetRequestPermissionMixin,
    generics.RetrieveAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer
    lookup_field = 'pk'

rulesetrequest_detail_view = RuleSetRequestDetailAPIView.as_view()

class RuleSetRequestApprovalAPIView(
    RuleSetRequestPermissionMixin,
    generics.RetrieveAPIView):
    queryset = RuleSetRequest.objects
    serializer_class = RuleSetRequestSerializer
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != RuleSetRequest.REQUESTED:
            return Response(f'Current status ({instance.status}) can\'t be changed', status=status.HTTP_400_BAD_REQUEST)
        if instance.approver != request.user:
            return Response('You are not the defined approver', status=status.HTTP_401_UNAUTHORIZED)
        
        rules = Rule.objects.get_rules_from_rule_set_request(instance)
        rule_status = ''
        path = request.get_full_path()
        if path.endswith('/approve/'):
            instance.status = RuleSetRequest.APPROVED
            rule_status = Rule.APPROVED
        elif path.endswith('/refuse/'):
            instance.status = RuleSetRequest.REFUSED
            rule_status = Rule.REFUSED
        else:
            return Response('Not a valid request', status=status.HTTP_400_BAD_REQUEST)
        for rule in rules:
            rule.set_status(rule_status, request.user)
        rule_serializer = RuleSerializer(context=self.get_serializer_context(), data=rules, many=True)
        if rule_serializer.is_valid():
            rule_serializer.save()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

rulesetrequest_approval_view = RuleSetRequestApprovalAPIView.as_view()