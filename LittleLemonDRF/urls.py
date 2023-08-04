"""
URL configuration for LittleLemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('menu-items', views.menu_item_list),
    path('menu-items/<str:menuItem>', views.menu_single_item_list),
    path('groups/manager/users', views.manager_users),
    path('groups/manager/users/<int:userId>', views.manager_users_single),
    path('groups/delivery-crew/users', views.delivery_crew_users),
    path('groups/delivery-crew/users/<int:userId>', views.delivery_crew_users_single),
    path('cart/menu-items', views.cart_menu_item),
    path('orders', views.orders),
    path('orders/<int:orderId>', views.single_order),

]
