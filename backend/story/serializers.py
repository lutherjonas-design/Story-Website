from rest_framework import serializers
from .models import Storys

class StorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storys
        fields = ["id", "title", "description"]
