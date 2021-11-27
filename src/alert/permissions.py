from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework import permissions

from alert.models import Contributors, Projects, Issues
from rest_framework.response import Response


# class IsUserAuthorAndIsAuthenticated(BasePermission):
# class IsUserAuthor(BasePermission):
#     """Vérification si l'utilisateur est auteur d'un projet avant affichage"""
#     message = "Permission refusée : l'utilisateur n'est pas auteur du projet"
#
#     # def has_permission(self, request, view):
#     #     if request.user.is_authenticated:
#     #         return True
#     #     return False
#
#     def has_object_permission(self, request, view, obj):
#         print("acces permissions")
#         print("view : ", view)
#         print("obj : ", obj)
#         print(request.user)
#         if Contributors.objects.filter(project=obj.pk, user=request.user, role="Author"):
#             return True
#         return False

# class AuthorIsRequestUserPermissions(BasePermission):
#     """Vérification si l'utilisateur est auteur d'un object avant affichage"""
#     message = "Permission refusée :Vous n'avez pas les droits requis sur cet objet"
#     # edit_methods = ("PUT", "DELETE")
#
#     def has_permission(self, request, view):
#
#         print("view : ", view)
#         print(request.user)
#         print(view.kwargs)
#     #     if request.user.is_authenticated:
#     #         print("request.user.is_authenticated")
#     #         return True
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         print("obj : ", obj)
#         print(permissions.SAFE_METHODS)
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         if obj.author_user == request.user:
#             return True
#
#         return False

########
class ProjectIsUserAuthorOrContributorPermissions(BasePermission):
    """Vérification si l'utilisateur est auteur d'un projet ou un contributeur
     et attribution de permissions différentes en fonction"""

    # Ici la permission fonctionne sans appel spécifique dans la vue car gérée
    # automatiquement par le ModelVieSet et les classes permissions.

    message = "Permission refusée : seul l'auteur ou le contributeur peuvent accéder" \
              " au détail d'un projet. Seul l'auteur peut le supprimer ou le modifier."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print("au niveau has obj perm")
        # le super user à tous pouvoirs
        if request.user.is_superuser:
            return True

        # AU NIVEAU DES OBJETS 'PROJETS' (MODEL PRODJECTS)
        # Recherche des auteurs ou contributeurs d'un projet au travers du model Contributors
        # est auteur :
        author = Contributors.objects.filter(project=obj.pk, user=request.user, role="Author")
        # est contributeur :
        contributor = Contributors.objects.filter(project=obj.pk, user=request.user,
                                                  role="Contributor")


        # Si le request user est l'auteur du projet, accès au CRUD complet
        if author:
            return True

        # Si le request user est un contributeur, accès seulement au R du CRUD,
        # donc au GET disponible par défaut dans SAFE_METHODS
        # (qui comprend aussi HEAD et OPTIONS mais sans conséquence)
        if contributor and request.method in permissions.SAFE_METHODS:
            return True

        return False


class IssuesPermissions(BasePermission):
    """Vérification que le request User est habilité à créer un problème.
    Vérification si l'utilisateur est auteur de l'objet ou contributeur et permissions adaptées
     en fonction"""

    # Attention : ici la permission ne fonctionne pas sans appel spécifique dans la vue,
    # car pas gérée automatiquement par le ModelVieSet et les classes permissions.
    # Seules les vues génériques (comme pour les projets) gèrent automatiquement
    # .check_object_permissions(request, obj)

    message = "Permission refusée : seul l'auteur de ce problème peut le supprimer ou le modifier"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        # AU NIVEAU DES OBJETS 'PROBLEMES' (MODEL ISSUES)
        author_methods = ("GET", "PUT", "DELETE")
        contributor_methods = ("PUT", "DELETE")

        # le super user à tous pouvoirs
        if request.user.is_superuser:
            return True

        # La création d'un problème n'est permise que si request user est auteur ou
        # contributeur d'un projet (indifféremment, donc pas besoin d'aller dans Contributors)
        # Recherche de author_user de projet
        project = Projects.objects.get_object_or_404(pk=view.pk)
        user_from_project = project.author_user

        # Si le request user un contributeur (au sens large, auteur ou contributeur)
        # du projet, création d'un problème associé possible
        if request.user == user_from_project and request.method == "POST":
            return True

        # Si le request user est l'auteur du problème, accès au RUD de CRUD
        if obj.author_user == request.user and request.method in self.author_methods:
            return True

        # Si le request user est le conributeur du problème, accès au UD de CRUD
        if obj.assignee_user == request.user and request.method in self.contributor_methods:
            return True


class CommentsPermissions(BasePermission):
    """Vérification que le request User est habilité à créer un commentaire.
    Vérification si l'utilisateur est auteur de l'objet ou contributeur et permissions adaptées
     en fonction"""

    # Attention : ici la permission ne fonctionne pas sans appel spécifique dans la vue,
    # car pas gérée automatiquement par le ModelVieSet et les classes permissions.
    # Seules les vues génériques (comme pour les projets) gèrent automatiquement
    # .check_object_permissions(request, obj)

    message = "Permission refusée : seul l'auteur de ce commentaire peut" \
              " le supprimer ou le modifier"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        # AU NIVEAU DES OBJETS 'COMMENTAIRES' (MODEL COMMENTS)
        author_methods = ("GET", "PUT", "DELETE")
        contributor_methods = ("PUT", "DELETE")

        # le super user à tous pouvoirs
        if request.user.is_superuser:
            return True

        # La création d'un commentaire n'est permise que si request user est auteur ou
        # contributeur d'un problème
        # Recherche de author_user du problème
        issue = Issues.objects.get_object_or_404(pk=request.query_params["issue_id"])
        author_from_issue = issue.author_user
        contributor_from_issue = issue.assignee_user

        # Si le request user un contributeur (au sens large, auteur ou contributeur)
        # du problème, création d'un commentaire associé possible
        if request.user == (author_from_issue or contributor_from_issue)\
                and request.method == "POST":
            return True

        # Si le request user est l'auteur du commentaire, accès au RUD de CRUD
        if obj.author_user == request.user and request.method in self.author_methods:
            return True

        # Particularité d'un commentaire par rapport à un problème,
        # le contributeur est ici l'auteur ou le contributeur du projet associé
        # au problème
        # Recherche de author_user du projet
        project = Projects.objects.get_object_or_404(pk=view.pk)
        user_from_project = project.author_user

        # Si le request user est le user_from_project accès au UD de CRUD
        if request.user == user_from_project and request.method in self.contributor_methods:
            return True

        return False
