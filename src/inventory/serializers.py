from rest_framework import serializers
from .models import Item

class ItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity']

class ItemOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"