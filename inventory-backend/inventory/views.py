from django.shortcuts import render
from django.db.models import F 
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .models import StockHistory, Item, Category
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CategorySerial, ItemSerial


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerial
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerial
    permission_classes = [IsAuthenticated]

    filter_field = ['category']
    search_field = ['name', 'description']
    ordering_field = ['quantity', 'created_at']

    def get_queryset(self):
        queryset = Item.objects.filter(owner=self.request.user)
        low = self.request.query_param.get('low')
        if low == 'true':
            queryset = queryset.filter(quantity__lte=F('low_stock'))
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_quantity = instance.quantity

        updated_item = serializer.save()
        new_quantity = updated_item.quantity

        updated_item = serializer.save()
        new_quantity = updated_item.quantity

        if old_quantity != new_quantity:
            StockHistory.objects.create(
                item=updated_item,
                changed_by=self.request.user,
                old=old_quantity,
                new=new_quantity
            )
    
    def update(self, request, *args, **kwargs):
        new_qty = request.data.get('quantity')
        if new_qty is not None and int(new_qty) < 0:
            return Response(
                {"detail": "Stock Level cannot be negative"},
                status = status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)