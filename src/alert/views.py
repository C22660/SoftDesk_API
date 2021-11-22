from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from alert.models import Projects, Contributors, Issues, Comments
from alert.serializers import ProjectsListSerializer, ProjectsDetailSerializer,\
    ContributorsSerializer, IssuesSerializer, CommentsSerializer

# 3 Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté
# !!! manque utilisateur connecté
# 5 Récupérer les détails d'un projet (project) via son id


class ProjectsViewset(ModelViewSet):

    # serializer_class = ProjectsListSerializer
    # detail_serializer_class = ProjectsDetailSerializer
    # permission_classes = [IsAuthenticated, IsUserAuthor]
    # permission_classes = [IsUserAuthor]

    serializer_class = ProjectsDetailSerializer

    def get_queryset(self):
        print("self.request.user ", self.request.user)
        return Projects.objects.all()
        # Pour récupérer les projets rattachés à l'user (soit auteur, soit contributeur)
        # return Projects.objects.filter(author_user=self.request.user)

    # Pour pouvoir faire un update partiel
    # https://tech.serhatteker.com/post/2020-09/enable-partial-update-drf/
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    # Surcharge du class DestroyModelMixin pour modifier le message retourné
    # à l'origine "return Response(status=status.HTTP_204_NO_CONTENT)"
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Le projet et ses problèmes associés ont bien été supprimés."},
                        status=200)

    # -----------CONTRIBUTORS---------------

    # Via @action, création de l'url : /projects/<id>/users (ici, users est automatiquement le nom
    # de la fonction, car aucun url_path de précisé)
    # sources : https://stackoverflow.com/questions/67927493/djangorestframework-create-separate-urls-for-separate-functions-of-modelviewse
    @action(detail=True, methods=['get', 'post'])
    def users(self, request, pk=None):
        """Création d'un path /projects/<id>/users pour afficher les contributeurs sur un projet,
        et enregistrer de nouveaux contributors"""
        if request.method == "GET":
            queryset = Contributors.objects.filter(project=pk)
            if len(queryset) == 0:
                raise Http404(f"Aucun projet {pk} n'a de contributeur.")

            serializer = ContributorsSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        # Ajout d'un contributeur :
        if request.method == "POST":
            # Vérification que le projet existe
            try:
                project = Projects.objects.get(pk=pk)
            except Projects.DoesNotExist:
                return HttpResponse({f"Le projet {pk} n'existe pas."}, status=404)

            # Si vérification passée :
            # Informations partielles adressées au sérializer (pas le projet puisque abs du body)
            serializer = ContributorsSerializer(data=request.data,
                                                partial=True)
            if serializer.is_valid():
                # Si Informations partielles validées :
                # Création du contributeur par le serializer en lui adressant le projet récupéré
                # dans le try précédent, grace au pk de l'url
                contributor = serializer.create(project=project)
                return Response(contributor, status=200)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Via @action, création de l'url : /project/{id}/users/{id}/ ici, l'url n'est pas le nom de
    # la fonction mais remplacé par url_path. Comme pk, user_id devient récupérable
    @action(detail=True, methods=['delete'], url_path='users/(?P<user_id>\d+)')
    def remove_contributor_from_project(self, request, user_id, pk=None):
        print(user_id)
        # Vérification que le projet existe
        try:
            Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return HttpResponse({f"Le projet {pk} n'existe pas."}, status=404)

        # récupération des contributions liées au projet et à l'user (auteur et contributeur)
        contribution_concerned = Contributors.objects.filter(project=pk).filter(user=user_id)

        # Si ce contibuteur n'est pas associé à ce projet, alors len = 0 :
        if len(contribution_concerned) == 0:
            return HttpResponse({f"Aucun contributeur {user_id} associé au projet {pk}."},
                                status=404
                                )
        else:
            for contribution in contribution_concerned:
                contribution.delete()

        return Response({"message": "L'utilisateur a bien été supprimé de ce projet."}, status=200)

    # -----------ISSUES------------------------------------------------------------

    # GET: /project/{id}/issues/
    @action(detail=True, methods=['get', 'post'])
    def issues(self, request, pk=None):
        """Création d'un path /projects/<id>/issues pour afficher les problèmes d'un projet,
        et en enregistrer de nouveaux """
        # récupération de <id> du projet dans /projects/<id>/issues via pk
        if request.method == "GET":
            # Vérification qu'il y a un problème d'enregisté sur le projet
            try:
                queryset = Issues.objects.get(project=pk)
            except Issues.DoesNotExist:
                return HttpResponse({"Aucun problème pour ce projet, ou projet inexistant."},
                                    status=404)

            serializer = IssuesSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        # Enregistrer un problème pour un projet
        if request.method == "POST":
            # Vérification que le projet existe
            try:
                project = Projects.objects.get(pk=pk)
            except Projects.DoesNotExist:
                return HttpResponse({f"Le projet {pk} n'existe pas."}, status=404)

            # Si vérification passée :
            # Informations partielles adressées au sérializer (pas le projet puisque abs du body et
            # présent dans l'url)
            serializer = IssuesSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                # Si Informations partielles validées :
                # Enregistrement du problème par le serializer en lui adressant le projet récupéré
                # dans le try précédent, grace au pk de l'url
                issue = serializer.create(project=project)
                return Response(issue, status=200)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Via @action, création de l'url : /project/{id}/issues/{id}/ ici, l'url n'est pas le nom de
        # la fonction mais remplacé par url_path. Comme pk, issue_id devient récupérable
    @action(detail=True, methods=['put', 'delete'], url_path='issues/(?P<issue_id>\d+)')
    def update_or_delete_issue(self, request, issue_id, pk=None):
        """Création d'un path /projects/<id>/issues/<id> pour mettre à jour un problème,
        ou le supprimer"""
        # Vérification que le projet existe
        try:
            Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return HttpResponse({f"Le projet {pk} n'existe pas."}, status=404)

        # récupération des problèmes liés au projet
        issue_concerned = Issues.objects.filter(project=pk).filter(pk=issue_id)
        # Si aucun problème n'est associé à ce projet, alors len = 0 :
        print(len(issue_concerned))
        if len(issue_concerned) == 0:
            return HttpResponse({f"Aucun problème {issue_id} associé au projet {pk}."},
                                status=404
                                )

        if request.method == "PUT":
            serializer = IssuesSerializer(partial=True)

            # Pas de création d'un update dans le serializers.py car utilisation de ipdate()
            issue_modified = serializer.update(instance=issue_concerned.first(),
                                               validated_data=request.query_params)

            # reserialization de issue_modified pour passage en Response
            issue_serialized = IssuesSerializer(instance=issue_modified).data

            return Response(issue_serialized, status=200)

        if request.method == "DELETE":
            issue_concerned.delete()

            return Response({"message": "Le problème a bien été supprimé."}, status=200)

        # -----------COMMENTS---------------------------------------------

        # Via @action, création de l'url : /project/{id}/issues/{id}/comments/
        # ici, l'url n'est pas le nom de la fonction mais remplacé par url_path.
        # Comme pk, issue_id devient récupérable
    @action(detail=True, methods=['post', 'get'],
            url_path='issues/(?P<issue_id>\d+)/comments')
    def comments(self, request, issue_id, pk=None):
        """Création d'un path /projects/<id>/issues/<id>/comments pour créer, récupérer
         un commentaire"""
        # Vérification que le problème existe
        try:
            issue_concerned = Issues.objects.get(pk=issue_id)
        except Issues.DoesNotExist:
            return HttpResponse({f"Le problème {issue_id} n'existe pas."}, status=404)

        # Enregistrer un commentaire pour un problème
        if request.method == "POST":
            # Informations partielles adressées au sérializer (pas l'ID de l'issue puisque abs
            # du body et présent dans l'url). Ci-dessous, request.data est vide, donc utilisation
            # de request.query_params
            serializer = CommentsSerializer(data=request.query_params, partial=True)
            if serializer.is_valid():
                # Si Informations partielles validées :
                # Enregistrement du commentaire par le serializer en lui adressant l'issue concernée
                # dans le try précédent, grace au issue_id de l'url
                comment = serializer.create(issue_concerned=issue_concerned)
                return Response(comment, status=200)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les commentaires d'un problème
        if request.method == 'GET':
            # récupération des commentaires liés à une issue
            all_comments_for_issue = Comments.objects.filter(issue=issue_id)
            datas = []
            for comment in all_comments_for_issue:
                serializer = CommentsSerializer(comment)
                datas.append(serializer.data)

            return Response(datas, status=200)

    @action(detail=True, methods=['get', 'put', 'delete'],
            url_path='issues/(?P<issue_id>\d+)/comments/(?P<comment_id>\d+)')
    def update_or_delete_or_get_comment(self, request, issue_id, comment_id, pk=None):
        """Création d'un path /projects/<id>/issues/<id>/comments pour créer, récupérer,
        modifier, supprimer un commentaire"""
        # Vérification qu'il y a un problème d'enregisté sur le projet
        try:
            Issues.objects.get(project=pk)
        except Issues.DoesNotExist:
            return HttpResponse({"Aucun problème pour ce projet, ou projet inexistant."},
                                status=404)
        # Vérification que le commentaire existe
        try:
            comment_concerned = Comments.objects.get(pk=comment_id)
        except Comments.DoesNotExist:
            return HttpResponse({f"Le commentaire {comment_id} n'existe pas."}, status=404)

        # Modifier un commentaire
        if request.method == "PUT":
            serializer = CommentsSerializer(partial=True)

            # Pas de création d'un update dans le serializers.py car utilisation de update()
            comment_modified = serializer.update(instance=comment_concerned,
                                                 validated_data=request.query_params)

            # reserialization de comment_modified pour passage en Response
            comment_serialized = CommentsSerializer(instance=comment_modified).data

            return Response(comment_serialized, status=200)

        if request.method == "DELETE":
            comment_concerned.delete()

            return Response({"message": "Le commentaire a bien été supprimé."}, status=200)
