from rest_framework import serializers

from .models import FirewallObject
from api.serializers import HistoricalRecordSerializer


class FirewallObjectSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='firewall-detail',
        lookup_field='pk',
        read_only = True
        )
    history = HistoricalRecordSerializer(read_only=True)

    class Meta:
        model = FirewallObject
        fields = [
            'hostname',
            'vendor',
            'detail_url',
            'history'
        ]


class FirewallObjectShortSerializer(serializers.ModelSerializer):

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