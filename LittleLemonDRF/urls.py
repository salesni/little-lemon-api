from django.urls import path, include
from rest_framework.routers import DefaultRouter
from LittleLemonDRF import views

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet, basename='menuitem')
router.register(r'cart/menu-items', views.CartViewSet, basename='cart')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
