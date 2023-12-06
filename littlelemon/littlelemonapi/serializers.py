from rest_framework import serializers

from decimal import Decimal

from .models import Category
from .models import MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    stock = serializers.IntegerField(source='inventory')
    taxed_price = serializers.SerializerMethodField(
        method_name='get_taxed_price'
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'price', 'stock',
                  'taxed_price', 'category_id']

    # Computed field
    @staticmethod
    def get_taxed_price(product: MenuItem):
        return product.price * Decimal(1.095)
