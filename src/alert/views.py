from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from alert.models import Projects, Contributors, Issues
from authentication.models import Users
from alert.serializers import ProjectsListSerializer, ProjectsDetailSerializer,\
    ContributorsSerializer, IssuesSerializer
from alert.permissions import IsUserAuthor

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

    # pour afficher soit le détail, soit la lste
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


    # def partial_update(self, request, pk=None):
    #     serialized = detail_serializer_class(request.user, data=request.data, partial=True)
    #     return Response(status=status.HTTP_202_ACCEPTED)

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
    def remove_contributor_from_project(self, user_id, pk=None):
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

    # -----------ISSUES---------------

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

            issue_serialized = IssuesSerializer(instance=issue_modified).data

            # print("type projet", type(projet))
            # print("type issue concernée : ", type(issue_concerned))
            # print("issue concernée : ", issue_concerned.first())
            # print("issue modifiée : ", issue_modified)
            # # print("request data : ", self.data)
            # print("request query_params : ", request.query_params)
            return Response(issue_serialized, status=200)




    # @action(
    #     detail=False,
    #     methods=["get"],
    #     name="Get email messages",
    #     url_path=r'some-prefix/(?P<email>\w+)',
    #     url_name="Email's messages"
    # )
    # def email_messages(self, request, email=None):
    #     return Response({"aaa": email}, status=200)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorsSerializer

    def get_queryset(self):
        print("self.request.user ", self.request.user)
        return Contributors.objects.all()


class IssuesViewset(ModelViewSet):

    serializer_class = IssuesSerializer

    def get_queryset(self):
        print("self.request.user ", self.request.user)
        return Issues.objects.all()

