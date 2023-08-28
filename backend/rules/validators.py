from rest_framework import serializers

from ipaddress import (
    ip_address,
    ip_network,
)

from .models import Rule

def validate_ip(value):
    try:
        obj = ip_address(value)
        return obj
    except ValueError as e:
        try:
            obj = ip_network(value)
            return obj
        except ValueError as ee:
            raise serializers.ValidationError(f"Validation-Error: {e}, {ee}")