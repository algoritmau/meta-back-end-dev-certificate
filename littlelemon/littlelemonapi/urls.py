from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-categories', views.menu_categories),
    path('categories/<int:pk>', views.category_details, name='category-detail'),
    path('menu-items', views.menu_items),
    path('menu-items/<int:menu_item_id>', views.single_menu_item),
    path('api-token-auth/', obtain_auth_token),
    path('secret/', views.secret_page),
    path('manager-only/', views.manager_only),
    path('anon-throttle-check/', views.anon_throttle_check),
    path('user-throttle-check/', views.user_throttle_check),
]
