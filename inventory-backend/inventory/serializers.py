from rest_framework import serializers
from .models import Category, Item

class CategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerial(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'quantity',
            'category',
            'low_stock',
            'created_at'
        ]

        read_only_fields = ['created_at']

    
    def validate(self, value):
        if value < 0:
            raise serializers.ValidationError('Quantity cannot be negative')
        return value
    

    