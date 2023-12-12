from rest_framework.decorators import api_view
# from rest_framework import generics
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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
    serialized_categories = CategorySerializer(categories, many=True)

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
        category_name = request.query_params.get('category', None)
        max_price = request.query_params.get('max_price', None)
        search_keyword = request.query_params.get('search', None)
        ordering = request.query_params.get('order_by', None)
        page = request.query_params.get('page', default=1)
        perpage = request.query_params.get('perpage', default=2)

        if category_name is not None:
            items = items.filter(category__slug=category_name)

        if max_price is not None:
            items = items.filter(price__lte=max_price)

        if search_keyword is not None:
            items = items.filter(name__icontains=search_keyword)

        if ordering is not None:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        # Pagination
        paginator = Paginator(items, perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_items = MenuItemSerializer(
            items,
            many=True,
            context={'request': request}
        )

        return Response(serialized_items.data)

    # Create new menu item record using deserialized data
    elif request.method == 'POST':
        new_item = MenuItemSerializer(data=request.data)

        if not new_item.is_valid():
            return Response(new_item.errors, status=400)

        new_item.save()

        return Response(new_item.data, status=201)


@api_view()
def single_menu_item(_request, menu_item_id):
    # menu_item = MenuItem.objects.get(pk=id)
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    serialized_menu_item = MenuItemSerializer(menu_item)

    return Response(serialized_menu_item.data)


# Protected view
@api_view()
@permission_classes([IsAuthenticated])
def secret_page(_request):
    return Response({'message': 'You have reached the secret page.'})


# Manager-only view
@api_view()
@permission_classes([IsAuthenticated])
def manager_only(_request):
    if _request.user.groups.filter(name='Management').exists():
        return Response({'message': 'You are a manager.'})
    else:
        return Response({'message': 'You are not a manager.'}, 403)
