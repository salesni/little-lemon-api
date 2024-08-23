
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('api/users/', views.CreateUserView.as_view(), name='create'),
    path('token/login/', views.CreateTokenView.as_view(), name='token'),
    path('api/users/users/me/', views.ManageUserView.as_view(), name='me'),
]