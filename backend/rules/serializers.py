from rest_framework import serializers
#from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer

from .models import Rule, FirewallObject
from . import validators


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only = True
        )
    title = serializers.CharField(read_only = True)


class FirewallObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = FirewallObject
        fields = [
            'hostname'
        ]

    
class RuleSerializer(serializers.ModelSerializer):
    #related_products = ProductInlineSerializer(source = "user.product_set.all", read_only = True, many = True)
    #edit_url = serializers.SerializerMethodField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='rule-detail',
        lookup_field='pk'
        )
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='rule-edit',
        lookup_field='pk'
        )
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='rule-delete',
        lookup_field='pk'
        )
    source_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    source_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    last_updated_by = UserPublicSerializer(read_only=True)
    created_by = UserPublicSerializer(read_only=True)
    # TODO make firewalls not writable but usable in Rule
    firewalls = FirewallObjectSerializer(many=True)
    class Meta:
        model = Rule
        # fields = '__all__'
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
            'delete_url'
        ]

    # def get_my_user_data(self, obj):
    #     return {
    #         "username": obj.user.username
    #     }


    def validate(self, data):
        if not data.get('source_ip_orig') and not data.get('source_ip_nat'):
            raise serializers.ValidationError('at least one source input is required')
        if not data.get('destination_ip_orig') and not data.get('destination_ip_nat'):
            raise serializers.ValidationError('at least one destination input is required')
        return data


    # def get_edit_url(self, obj) -> str:
    #     # return f"/api/rules/{obj.pk}/update/"
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("rule-edit", kwargs={"pk": obj.pk}, request=request)