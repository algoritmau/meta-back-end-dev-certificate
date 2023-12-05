from rest_framework import serializers

from decimal import Decimal

from .models import Category
from .models import MenuItem


# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=5, decimal_places=2)
#     inventory = serializers.IntegerField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    # Create new stock field based on inventory
    stock = serializers.IntegerField(source='inventory')
    taxed_price = serializers.SerializerMethodField(
        method_name='get_taxed_price'
    )
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='category-detail'
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'price', 'stock',
                  'taxed_price']

    # Computed field
    @staticmethod
    def get_taxed_price(product: MenuItem):
        tax_rate = Decimal(1.095)

        return product.price * tax_rate
