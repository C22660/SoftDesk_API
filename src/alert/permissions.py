from rest_framework.permissions import BasePermission
from rest_framework import permissions

from alert.models import Contributors, Projects, Issues, Comments


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
    # view.kwargs["pk"] idem obj.pk, soit l'ID du projet

    message = "Permission refusée : seul un auteur ou contributeur du projet concerné " \
              "peut créer un Problème. " \
              "Seul l'auteur ou contributeur d'un problème peut le visualiser. " \
              "Seul l'auteur peut le supprimer ou le modifier."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print("has_object_permission issue")
        # AU NIVEAU DES OBJETS 'PROBLEMES' (MODEL ISSUES)
        author_methods = ("GET", "PUT", "DELETE")
        contributor_methods = ("GET",)

        # le super user à tous pouvoirs
        if request.user.is_superuser:
            return True

        # La création d'un problème n'est permise que si request user est auteur ou
        # contributeur d'un projet (indifféremment, donc pas besoin d'aller dans Contributors)
        # Recherche des auteurs ou contributeurs d'un projet au travers du model Contributors
        # est auteur :
        author_from_project = Contributors.objects.filter(project=view.kwargs["pk"],
                                                          user=request.user,
                                                          role="Author")
        # est contributeur :
        contributor_from_project = Contributors.objects.filter(project=view.kwargs["pk"],
                                                               user=request.user,
                                                               role="Contributor")

        # Recherche des auteurs ou contributeurs d'un problème au travers du model Issues
        # est auteur :
        author_from_issue = Issues.objects.filter(project=obj.pk, author_user=request.user)
        # est contributeur :
        contributor_from_issue = Issues.objects.filter(project=obj.pk, assignee_user=request.user)

        # Si le request user un contributeur (au sens large, auteur ou contributeur)
        # du projet, création d'un problème associé possible
        if (author_from_project or contributor_from_project) and request.method == "POST":
            return True

        # Si le request user est l'auteur du problème, accès au RUD de CRUD
        if author_from_issue and request.method in author_methods:
            return True

        # Si le request user est le contributeur du problème, accès au R de CRUD
        if contributor_from_issue and request.method in contributor_methods:
            return True

        return False


class CommentsPermissions(BasePermission):
    """Vérification que le request User est habilité à créer un commentaire.
    Vérification si l'utilisateur est auteur de l'objet ou contributeur et permissions adaptées
     en fonction"""

    # Attention : ici la permission ne fonctionne pas sans appel spécifique dans la vue,
    # car pas gérée automatiquement par le ModelVieSet et les classes permissions.
    # Seules les vues génériques (comme pour les projets) gèrent automatiquement
    # .check_object_permissions(request, obj)

    message = "Permission refusée : seul un auteur ou contributeur du problème concerné " \
              "peut créer un commentaire. " \
              "Seul l'auteur du commentaire ou contributeur du projet peut le visualiser. " \
              "Seul l'auteur du commentaire peut le supprimer ou le modifier."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        print("has_object_permission comment")
        print(request.user)

        # AU NIVEAU DES OBJETS 'COMMENTAIRES' (MODEL COMMENTS)
        author_methods = ("GET", "PUT", "DELETE")
        contributor_methods = ("GET", "POST")

        # le super user à tous pouvoirs
        if request.user.is_superuser:
            return True

        # La création d'un commentaire n'est permise que si request user est auteur ou
        # contributeur d'un problème
        # Recherche de author_user du problème
        author_from_issue = Issues.objects.filter(project=obj.pk, author_user=request.user)
        # est contributeur :
        contributor_from_issue = Issues.objects.filter(project=obj.pk, assignee_user=request.user)

        # Si le request user est contributeur (au sens large, auteur ou contributeur)
        # du problème, création d'un commentaire associé possible
        if (author_from_issue or contributor_from_issue) and request.method == "POST":
            return True

        # Si le request user est l'auteur du commentaire, accès au RUD de CRUD
        # Recherche de l'auteur du commentaire au travers du model Comments
        # est auteur :
        author_from_comment = Comments.objects.filter(issue=view.kwargs["issue_id"],
                                                      author_user=request.user)

        if author_from_comment and request.method in author_methods:
            return True

        # Particularité d'un commentaire par rapport à un problème,
        # le contributeur est ici l'auteur ou le contributeur du projet associé
        # au problème
        # Recherche de author_user du projet
        # Recherche des auteurs ou contributeurs d'un projet au travers du model Contributors
        # est auteur :
        author_from_project = Contributors.objects.filter(project=view.kwargs["pk"],
                                                          user=request.user, role="Author")
        # est contributeur :
        contributor_from_project = Contributors.objects.filter(project=view.kwargs["pk"],
                                                               user=request.user,
                                                               role="Contributor")

        # Si le request user est le author_from_project ou contributot_from_project
        # accès au CR de CRUD
        if (author_from_project or contributor_from_project)\
                and request.method in contributor_methods:
            return True

        return False
