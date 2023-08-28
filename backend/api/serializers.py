from rest_framework import serializers

class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(read_only = True)