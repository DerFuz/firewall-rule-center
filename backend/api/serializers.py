from rest_framework import serializers

class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()

class HistoricalRecordSerializer(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())