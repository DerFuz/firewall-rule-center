from rest_framework import serializers
from django.contrib.auth import get_user_model, models

from .models import RuleSetRequest
from rules.serializers import RuleInlineSerializer
from api.serializers import UserPublicSerializer, HistoricalRecordSerializer

class RuleSetRequestSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='rulesetrequest-detail',
        lookup_field='pk',
        read_only = True
        )
    approve_url = serializers.HyperlinkedIdentityField(
        view_name='rulesetrequest-approve',
        lookup_field='pk',
        read_only = True
        )
    refuse_url = serializers.HyperlinkedIdentityField(
        view_name='rulesetrequest-refuse',
        lookup_field='pk',
        read_only = True
        )
    related_rules = RuleInlineSerializer(source='rule_rule_set_request.all', read_only=True, many=True)
    status = serializers.CharField(read_only=True)
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
            'approve_url',
            'refuse_url',
            'history',
        ]
    
    def validate_approver(self, data):
        # validates if nested approver-object exists, but does not create new ones
        try:
            approver_id = data.get('id')
            try:
                approver_obj = get_user_model().objects.get(id=approver_id)
                return approver_obj
            except models.User.DoesNotExist:
                raise serializers.ValidationError(f'Approver with id {approver_id} does not exist')
        except KeyError:
            return None