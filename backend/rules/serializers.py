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
    #my_user_data = serializers.SerializerMethodField(read_only = True) # bad
    #my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    #url = serializers.HyperlinkedIdentityField(
    #    view_name='product-detail',
    #    lookup_field='pk'
    #    )
    #title = serializers.CharField(validators=[
    #    validators.validate_title_no_hello,
    #    validators.unique_product_title
    #    ])
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

    def get_edit_url(self, obj):
        # return f"/api/rules/{obj.pk}/update/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("rule-edit", kwargs={"pk": obj.pk}, request=request)
    
    def get_delete_url(self, obj):
        # return f"/api/rules/{obj.pk}/delete/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("rule-delete", kwargs={"pk": obj.pk}, request=request)