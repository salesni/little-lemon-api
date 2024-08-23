from django.urls import path
from . import views

app_name = 'group'  # Ensure this namespace is unique

urlpatterns = [
    path('manager/users', views.ManagerGroupViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='manager-group'),
    path('delivery-crew/users', views.DeliveryCrewGroupViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='delivery-crew-group'),
]
