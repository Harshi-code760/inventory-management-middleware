from rest_framework import serializers
from .models import Category, Item

class CategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerial(serializers.ModelSerializer):
    is_low = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'description',
            'quantity',
            'category',
            'low_stock',
            'created_at',
            'is_low'
        ]

        read_only_fields = ['created_at']

    
    def validate(self, value):
        if value < 0:
            raise serializers.ValidationError('Quantity cannot be negative')
        return value
    
    def is_low(self, obj):
        return obj.quantity <= obj.low_stock
    

    