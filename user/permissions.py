from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery crew').exists()

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists()
