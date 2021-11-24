from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from alert.models import Contributors
from rest_framework.response import Response


class IsUserAuthorAndIsAuthenticated(BasePermission):
    """Vérification si l'utilisateur est auteur d'un projet avant affichage"""
    message = "L'utilisateur n'est pas auteur du projet"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if Contributors.objects.filter(project=obj.pk, user=request.user, role="Author"):
            return True
        return False
