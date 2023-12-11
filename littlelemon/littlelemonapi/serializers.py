from rest_framework import serializers

from decimal import Decimal

from rest_framework.validators import UniqueValidator

from .models import Category
from .models import MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        extra_kwargs = {
            'name': {
                'validators': [UniqueValidator(queryset=Category.objects.all())]
            }
        }


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    stock = serializers.IntegerField(source='inventory')
    taxed_price = serializers.SerializerMethodField(
        method_name='get_taxed_price'
    )

    def validate(self, attrs):
        if attrs['price'] < Decimal(2.0):
            raise serializers.ValidationError(
                'Minimum price must be at least $2.00.'
            )

        if attrs['inventory'] < 0:
            raise serializers.ValidationError(
                'Stock must be at least 0.'
            )

        return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'price', 'stock',
                  'taxed_price', 'category_id']
        extra_kwargs = {
            'name': {
                'validators': [UniqueValidator(queryset=MenuItem.objects.all())]
            }
        }

    # Computed field
    @staticmethod
    def get_taxed_price(product: MenuItem):
        return product.price * Decimal(1.095)
