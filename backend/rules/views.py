from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.db import transaction

import csv

from .models import Rule, RuleSetRequest
from .serializers import RuleSerializer
from api.mixins import RulePermissionMixin

class RuleListCreateAPIView(
    RulePermissionMixin,
    generics.ListCreateAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    
    def perform_create(self, serializer):
        data = {
            'created_by': self.request.user,
            'last_updated_by': self.request.user
        }
        serializer.save(**data)

rule_list_create_view = RuleListCreateAPIView.as_view()


class RuleDetailAPIView(
    RulePermissionMixin,
    generics.RetrieveAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = 'pk'

rule_detail_view = RuleDetailAPIView.as_view()


class RuleUpdateAPIView(
    RulePermissionMixin,
    generics.UpdateAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        data = {
            'last_updated_by': self.request.user
        }
        instance = serializer.save(**data)
        instance_rule_set_request = instance.rule_set_request
        # if status changes to configured (CON) and rule_set_request is set
        if instance.status == Rule.CONFIGURED and instance_rule_set_request is not None:
            # get all sibling-rules for this rule_set_request that are not configured (CON)
            siblings = Rule.objects.get_rules_from_rule_set_request(instance_rule_set_request).exclude(id=instance.id).exclude(status=Rule.CONFIGURED)
            # if none are found => all siblings configured (CON) => set RuleSetRequest to configured (CON)
            if siblings.count() == 0:
                rule_set_request = RuleSetRequest.objects.filter(id=instance_rule_set_request.id).first()
                rule_set_request.status = RuleSetRequest.CONFIGURED
                rule_set_request.save()

rule_update_view = RuleUpdateAPIView.as_view()


class RuleDestroyAPIView(
    RulePermissionMixin,
    generics.DestroyAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.soft_deleted(self.request.user)
        
rule_delete_view = RuleDestroyAPIView.as_view()


class RuleImportAPIView(
    RulePermissionMixin,
    generics.GenericAPIView):
    queryset = Rule.objects.none()
    serializer_class = RuleSerializer
    http_method_names = ['post', 'options']
    parser_classes = [FileUploadParser]
    
   
    # atomic transaction to only import rules if no error occurs
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {
            'created_by': self.request.user,
            'last_updated_by': self.request.user
        }
        
        # TODO better error handling
        
        # Request must include following header:
        # 'Content-Disposition: attachment; filename=<filename>'
        try:
            file_obj = request.data.get('file')
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            data_rows = []
            for row in reader:
                firewalls = [{'hostname': i } for i in row['firewalls'].split(',') if i != '']
                row['firewalls'] = firewalls
                row = {k : v for k, v in row.items() if v != ''}
                data_rows.append(row)
            
            # create one serializer for all rules
            serializer = RuleSerializer(context=self.get_serializer_context(), data=data_rows, many=True)
            if serializer.is_valid():
                serializer.save(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            errors = {f'Line {i} errors': errors for i, errors in enumerate(serializer.errors, 1) if len(errors) > 0}
            return Response([errors], status=status.HTTP_406_NOT_ACCEPTABLE)
        except (KeyError, AttributeError):
            return Response('Error reading file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
rule_import_view = RuleImportAPIView.as_view()