from rest_framework.decorators import api_view
# from rest_framework import generics
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#
# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


@api_view()
def menu_categories(_request):
    categories = Category.objects.all()
    serialized_categories = MenuItemSerializer(categories, many=True)

    return Response(serialized_categories.data)


@api_view()
def category_details(_request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)

    return Response(serialized_category.data)


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_items = MenuItemSerializer(
            items,
            many=True,
            context={'request': request}
        )

        return Response(serialized_items.data)

    # Create new menu item record using deserialized data
    elif request.method == 'POST':
        new_item = MenuItemSerializer(data=request.data)

        if new_item.is_valid():
            new_item.save()

            return Response(new_item.data, status=201)

        return Response(new_item.errors, status=400)


@api_view()
def single_menu_item(_request, menu_item_id):
    # menu_item = MenuItem.objects.get(pk=id)
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    serialized_menu_item = MenuItemSerializer(menu_item)

    return Response(serialized_menu_item.data)
