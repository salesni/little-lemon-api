from django.utils import timezone
from rest_framework import viewsets, permissions,status
from rest_framework.permissions import SAFE_METHODS
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from user.permissions import IsManager, IsCustomer, IsDeliveryCrew
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User = get_user_model()

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        if self.request.user.groups.filter(name='Manager').exists():
            return [IsManager()]
        return [permissions.IsAuthenticated(), IsCustomer()]
    
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menu_item_id = serializer.validated_data.get('menu_item_id')
        menu_item = MenuItem.objects.get(id=menu_item_id)
        
        quantity = serializer.validated_data.get('quantity', 1)
        unit_price = menu_item.price
        price = unit_price * quantity
        
        cart_item = serializer.save(
            user=self.request.user,
            menu_item=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsCustomer()]
    



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all().prefetch_related('items')
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user).prefetch_related('items')
        else:
            return Order.objects.filter(user=user).prefetch_related('items')
    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        items_data = [
            {
                'menu_item': cart_item.menu_item,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.menu_item.price,
                'price': cart_item.price,
            }
            for cart_item in cart_items
        ]

        order = serializer.save(user=user, items=items_data)
        cart_items.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsManager()]
        elif self.request.user.groups.filter(name='Manager').exists():
            return [permissions.IsAuthenticated(), IsManager()]
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            return [permissions.IsAuthenticated(), IsDeliveryCrew()]
        else:
            return [permissions.IsAuthenticated(), IsCustomer()]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user

        if user.groups.filter(name='Manager').exists():
            if 'delivery_crew' in request.data:
                delivery_crew_email = request.data['delivery_crew']
                try:
                    delivery_crew = User.objects.get(email=delivery_crew_email)
                    instance.delivery_crew = delivery_crew
                except User.DoesNotExist:
                    return Response({"detail": f"User with email {delivery_crew_email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.groups.filter(name='Delivery crew').exists():     
            if 'status' in request.data:
                instance.status = request.data['status']
        elif instance.user == user:
            # Allow customer to update their own order
            pass
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)