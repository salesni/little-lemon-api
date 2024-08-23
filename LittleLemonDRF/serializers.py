from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from .models import Category, MenuItem, Cart, OrderItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = [ 'id','title','price','stock','price_after_tax', 'category','category_id']

    def calculate_tax(self,product:MenuItem):
        return product.price * Decimal(1.1)

class CartSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item','menu_item_id', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'unit_price': {'read_only': True},
            'price': {'read_only': True}
        }




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(user=validated_data['user'], total=0.0, date=timezone.now().date())

        total = Decimal('0.00')
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            unit_price = menu_item.price
            price = unit_price * quantity
            total += price
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, unit_price=unit_price, price=price)

        order.total = total
        order.save()
        return order