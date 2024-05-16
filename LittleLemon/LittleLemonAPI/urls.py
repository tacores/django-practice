from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name='LittleLemonAPI'

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'groups/manager/users', views.ManagerUserViewSet, basename='manager-user')
router.register(r'groups/delivery-crew/users', views.DeliveryUserViewSet, basename='delivery-user')
router.register(r'cart/items', views.CartViewSet, basename='cart-items')
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [ 
    path('', include(router.urls)),
]
