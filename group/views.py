from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from user.permissions import IsManager, IsDeliveryCrew


User = get_user_model()

class ManagerGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        users = User.objects.filter(groups__name='Manager')
        return Response({"managers": [user.email for user in users]})

    def create(self, request):
        user = User.objects.get(id=request.data['user_id'])
        group = Group.objects.get(name='Manager')
        user.groups.add(group)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        group = Group.objects.get(name='Manager')
        user.groups.remove(group)
        return Response(status=status.HTTP_200_OK)

class DeliveryCrewGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        users = User.objects.filter(groups__name='Delivery crew')
        return Response({"delivery_crew": [user.email for user in users]})

    def create(self, request):
        user = User.objects.get(id=request.data['user_id'])
        group = Group.objects.get(name='Delivery crew')
        user.groups.add(group)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        group = Group.objects.get(name='Delivery crew')
        user.groups.remove(group)
        return Response(status=status.HTTP_200_OK)
