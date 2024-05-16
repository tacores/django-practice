from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import viewsets
from .permissions.custom_permissions import IsManager, IsDeliveryCrewOrManager, IsCustomerOrManager
from django.contrib.auth.models import User, Group

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

class ManagerUserViewSet(viewsets.ModelViewSet):
    group = Group.objects.get(name='manager')
    queryset = group.user_set.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

class DeliveryUserViewSet(viewsets.ModelViewSet):
    group = Group.objects.get(name='delivery crew')
    queryset = group.user_set.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        item_id = serializer.validated_data['menuitem'].id
        item = MenuItem.objects.get(pk=item_id)
        quantity = int(serializer.validated_data['quantity'])
        serializer.save(user=self.request.user, unit_price=item.price, price=item.price * quantity)

    def perform_update(self, serializer):
        item_id = serializer.validated_data['menuitem'].id
        item = MenuItem.objects.get(pk=item_id)
        quantity = int(serializer.validated_data['quantity'])
        serializer.save(user=self.request.user, unit_price=item.price, price=item.price * quantity)

    def get_permissions(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsCustomerOrManager]
        elif self.action in ['create']:
            permission_classes = [IsCustomerOrManager]
        elif self.action in ['destroy']:
            permission_classes = [IsCustomerOrManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_permissions(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            permission_classes = [IsCustomerOrManager]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsDeliveryCrewOrManager]
        elif self.action in ['destroy']:
            permission_classes = [IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            queryset = Order.objects.all()
        elif self.request.user.groups.filter(name='delivery crew').exists():
            queryset = Order.objects.filter(delivery_crew=self.request.user)
        else:
            queryset = Order.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        total = 0
        cart_items = Cart.objects.filter(user=self.request.user.id)
        for item in cart_items:
            total += item.price

        order = serializer.save(user=self.request.user, status=0, total=total)

        for item in cart_items:
            order_item = {
                'order': order.id,
                'menuitem': item.menuitem.id,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'price': item.price
            }
            item_serializer = OrderItemSerializer(data=order_item)
            if item_serializer.is_valid(raise_exception=True):
                item_serializer.save()
        
        Cart.objects.filter(user=self.request.user.id).delete()

        return order

