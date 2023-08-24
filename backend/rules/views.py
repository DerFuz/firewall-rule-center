from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Rule
from .serializers import RuleSerializer

class RuleListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def perform_create(self, serializer):
        serializer.save()
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
    generics.RetrieveAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    lookup_field = "pk"

rule_detail_view = RuleDetailAPIView.as_view()


class RuleUpdateAPIView(
    generics.UpdateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        #if not instance.content:
        #    instance.content = instance.title

rule_update_view = RuleUpdateAPIView.as_view()


class RuleDestroyAPIView(
    generics.DestroyAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)
        
rule_delete_view = RuleDestroyAPIView.as_view()