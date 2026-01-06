# api/serializers.py

from rest_framework import serializers
from .models import Wine

class WineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = '__all__'
        read_only_fields = ['id']  # Good practice