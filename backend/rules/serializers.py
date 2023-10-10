from rest_framework import serializers
#from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer, HistoricalRecordSerializer

from .models import Rule, FirewallObject
from . import validators


class RuleInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='rule-detail',
        lookup_field='pk',
        read_only = True
        )


class FirewallObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = FirewallObject
        fields = [
            'hostname'
        ]

        extra_kwargs = {
            'hostname': {'validators': []},
        }

        # TODO ensure uniqueness constraint for creation and update
        # https://stackoverflow.com/questions/38438167/unique-validation-on-nested-serializer-on-django-rest-framework/

    
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
    firewalls = FirewallObjectSerializer(required=False, many=True)
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
        if not data.get('source_ip_orig') and not data.get('source_ip_nat'):
            raise serializers.ValidationError('at least one source input is required')
        if not data.get('destination_ip_orig') and not data.get('destination_ip_nat'):
            raise serializers.ValidationError('at least one destination input is required')
        # validates that nested firewall-object exists, but does not create new ones
        firewalls_data = data.pop('firewalls')
        firewall_objs = []
        for firewall in firewalls_data:
            res = FirewallObject.objects.filter(hostname=firewall['hostname'])
            if not res:
                raise serializers.ValidationError(f'firewall-object for <{firewall["hostname"]}> does not exist')
            else:
                # append firewallobject, not firewallobjectqueryset
                firewall_objs.append(res[0])
        
        data.update({'firewalls': firewall_objs})   
        return data
    
    def create(self, validated_data):
        firewalls_data = validated_data.pop('firewalls')
        rule = Rule.objects.create(**validated_data)
        rule.firewalls.set(firewalls_data)
        return rule