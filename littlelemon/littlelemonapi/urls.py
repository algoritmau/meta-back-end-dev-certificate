from django.urls import path
from . import views

urlpatterns = [
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-categories', views.menu_categories),
    path('categories/<int:pk>', views.category_details, name='category-detail'),
    path('menu-items', views.menu_items),
    path('menu-items/<int:menu_item_id>', views.single_menu_item),
]
