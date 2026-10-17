from rest_framework import serializers
from .models import JokeStore


class JokeStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JokeStore
        fields = ['id', 'text', 'created_at', 'likes']
        read_only_fields = ['id', 'created_at']
