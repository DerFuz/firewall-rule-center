from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Rule
from . import validators


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only = True
        )
    title = serializers.CharField(read_only = True)


class RuleSerializer(serializers.ModelSerializer):
    #requester = UserPublicSerializer(source = "user", read_only = True) # good
    #related_products = ProductInlineSerializer(source = "user.product_set.all", read_only = True, many = True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    #url = serializers.HyperlinkedIdentityField(
    #    view_name='product-detail',
    #    lookup_field='pk'
    #    )
    source_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    source_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_orig = serializers.CharField(required=False, validators=[validators.validate_ip])
    destination_ip_nat = serializers.CharField(required=False, validators=[validators.validate_ip])
    class Meta:
        model = Rule
        fields = '__all__'
        #fields = [
        #    'pk',
        #    'action',
        #    'source',
        #    'destination',
        #    'protocol',
        #    'port',
        #    'status'
        #]

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


    def get_edit_url(self, obj) -> str:
        # return f"/api/rules/{obj.pk}/update/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("rule-edit", kwargs={"pk": obj.pk}, request=request)
    
    def get_delete_url(self, obj) -> str:
        # return f"/api/rules/{obj.pk}/delete/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("rule-delete", kwargs={"pk": obj.pk}, request=request)