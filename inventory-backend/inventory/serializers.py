from rest_framework import serializers
from .models import Category, Item, StockHistory

class CategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class StockHistorySerial(serializers.ModelSerializer):
    changed_by_name = serializers.ReadOnlyField(source='changed_by.username')

    class Meta:
        model = StockHistory
        fields = ['id', 'old', 'new', 'changed', 'changed_by_name']

class ItemSerial(serializers.ModelSerializer):
    is_low = serializers.SerializerMethodField()
    history = StockHistorySerial(many=True, read_only=True)

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
            'is_low',
            'history'
        ]

        read_only_fields = ['created_at']

    def get_is_low(self, obj):
        return obj.quantity <= obj.low_stock
    

    