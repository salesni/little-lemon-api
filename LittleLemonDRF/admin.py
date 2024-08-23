from django.contrib import admin
from .models import Cart, Order, MenuItem, Category,OrderItem

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MenuItem)
admin.site.register(Category)