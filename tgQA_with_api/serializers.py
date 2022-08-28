from rest_framework import serializers
from .models import *

class TGserializer(serializers.Serializer):
    tguser = serializers.CharField(max_length=50)
    question = serializers.CharField()
    answer = serializers.CharField(read_only=True)
    is_answered = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return TelegramQA.objects.create(**validated_data)
