from rest_framework import serializers
#from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer, HistoricalRecordSerializer

from .models import Rule
from firewalls.models import FirewallObject
from firewalls.serializers import FirewallObjectShortSerializer
from . import validators


class RuleInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='rule-detail',
        lookup_field='pk',
        read_only = True
        )

    
class RuleSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='rule-detail',
        lookup_field='pk',
        read_only = True
        )
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='rule-edit',
        lookup_field='pk',
        read_only = True
        )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='rule-delete',
        lookup_field='pk',
        read_only = True
        )
    source_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    source_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    last_updated_by = UserPublicSerializer(read_only=True)
    created_by = UserPublicSerializer(read_only=True)
    firewalls = FirewallObjectShortSerializer(required=False, many=True)
    history = HistoricalRecordSerializer(read_only=True)
    # TODO firewall m2m history
    
    class Meta:
        model = Rule
        fields = [
            'pk',
            'action',
            'protocol',
            'source_name',
            'source_ip_orig',
            'source_ip_nat',
            'source_port',
            'destination_name',
            'destination_ip_orig',
            'destination_ip_nat',
            'destination_port',
            'requester',
            'ticket',
            'rule_set_request',
            'notes',
            'firewalls',
            'status',
            'created_on',
            'created_by',
            'last_updated_on',
            'last_updated_by',
            'is_deleted',
            'detail_url',
            'edit_url',
            'delete_url',
            'history',
        ]

    def validate(self, data):
        # PATCH requests do not require any ip-field
        if self.context.get('request').method != 'PATCH':
            if not data.get('source_ip_orig') and not data.get('source_ip_nat'):
                raise serializers.ValidationError('at least one source input is required')
            if not data.get('destination_ip_orig') and not data.get('destination_ip_nat'):
                raise serializers.ValidationError('at least one destination input is required')
        return data
    
    def validate_firewalls(self, data):
        # validates if nested firewall-object exists, but does not create new ones
        firewall_objs = []
        for firewall in data:
            res = FirewallObject.objects.filter(hostname=firewall['hostname'])
            if not res:
                raise serializers.ValidationError(f'firewall-object for <{firewall["hostname"]}> does not exist')
            else:
                # append firewallobject, not firewallobjectqueryset
                firewall_objs.append(res[0])
        return firewall_objs
    
    def create(self, validated_data):
        try:
            firewalls_data = validated_data.pop('firewalls')
            rule = Rule.objects.create(**validated_data)
            rule.firewalls.set(firewalls_data)
        except KeyError:
            rule = Rule.objects.create(**validated_data)
        return rule
    
    def update(self, instance, validated_data):
        try:
            firewalls_data = validated_data.pop('firewalls')
            super().update(instance, validated_data)
            instance.firewalls.set(firewalls_data)
        except KeyError:
            super().update(instance, validated_data)
        return instance