from django.shortcuts import render
from django.db.models import F 
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Item
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