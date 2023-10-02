from rest_framework import serializers

from .models import RuleSetRequest
from rules.serializers import RuleInlineSerializer
from api.serializers import UserPublicSerializer, HistoricalRecordSerializer


class RuleSetRequestSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='rulesetrequest-detail',
        lookup_field='pk',
        read_only = True
        )
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='rulesetrequest-edit',
        lookup_field='pk',
        read_only = True
        )
    related_rules = RuleInlineSerializer(source='rule_rule_set_request.all', read_only=True, many=True)
    approver = UserPublicSerializer()
    last_updated_by = UserPublicSerializer(read_only=True)
    created_by = UserPublicSerializer(read_only=True)
    history = HistoricalRecordSerializer(read_only=True)


    class Meta:
        model = RuleSetRequest
        fields = [
            'pk',
            'related_rules',
            'status',
            'approver',
            'created_on',
            'created_by',
            'last_updated_on',
            'last_updated_by',
            'detail_url',
            'edit_url',
            'history',
        ]
