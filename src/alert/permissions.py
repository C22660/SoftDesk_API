from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from alert.models import Contributors
from rest_framework.response import Response


class IsUserAuthor(BasePermission):
    """Vérification si l'utilisateur est auteur d'un projet avant affichage"""
    message = "L'utilisateur n'est pas auteur d'un projet"
    print("hello")

    def has_object_permission(self, request, view, obj):
        # Ne donnons l’accès qu’aux contributeurs ayant un rôle d'auteur
        user = request.user
        contributions = get_object_or_404(Contributors, user=user.pk)
        for contribution in contributions:
            if contribution.author != user:
                return Response({'response': "Vous n'avez pas de créé de projet"})
