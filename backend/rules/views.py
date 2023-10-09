from rest_framework import generics, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.db import transaction

import csv

from .models import Rule
from .serializers import RuleSerializer
from api.mixins import RulePermissionMixin
from api.permissions import RulePermissions

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
        #serializer.save(user = self.request.user)
        # email = serializer.validated_data.pop('email')
        # print(email)
        # print(serializer.validated_data)
        #title = serializer.validated_data.get("title")
        #content = serializer.validated_data.get("content") or None
        #if content is None:
        #    content = title
        #serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     # not needed really, if we are sure that the user is authenticated, aka StaffEditorPermissionMixin
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)

rule_list_create_view = RuleListCreateAPIView.as_view()


class RuleDetailAPIView(
    RulePermissionMixin,
    generics.RetrieveAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = "pk"

rule_detail_view = RuleDetailAPIView.as_view()


class RuleUpdateAPIView(
    RulePermissionMixin,
    generics.UpdateAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        data = {
            'last_updated_by': self.request.user
        }
        instance = serializer.save(**data)
        #if not instance.content:
        #    instance.content = instance.title

rule_update_view = RuleUpdateAPIView.as_view()


class RuleDestroyAPIView(
    RulePermissionMixin,
    generics.DestroyAPIView):
    queryset = Rule.objects.exclude_deleted()
    serializer_class = RuleSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        instance.soft_deleted(self.request.user)
        
rule_delete_view = RuleDestroyAPIView.as_view()


class RuleImportAPIView(
    RulePermissionMixin,
    views.APIView):

    parser_classes = (FileUploadParser,)

    # atomic transaction to only import rules if no error occurs
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {
            'created_by': self.request.user,
            'last_updated_by': self.request.user
        }

        file_obj = request.data['file']
        decoded_file = file_obj.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        data_rows = []
        for row in reader:
            firewalls = [{"hostname": i } for i in row['firewalls'].split(',') ]
            row['firewalls'] = firewalls
            data_rows.append(row)

        # create one serializer for all rules
        serializer = RuleSerializer(data=data_rows, many=True)
        if serializer.is_valid():
            serializer.save(**data)
            return Response(status=204)
        return Response(status=406)
        
rule_import_view = RuleImportAPIView.as_view()