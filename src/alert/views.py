from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
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

    # -----------CONTrIBUTORS---------------

    # GET: /projects/<id>/users
    # sources : https://stackoverflow.com/questions/67927493/djangorestframework-create-separate-urls-for-separate-functions-of-modelviewse
    @action(detail=True, methods=['get', 'post'])
    def users(self, request, *args, **kwargs):
        """Création d'un path /projects/<id>/users pour afficher les contributeurs sur un projet,
        et enregistrer de nouveaux contributors"""
        # récupération de <id> du projet dans /projects/<id>/users via params['pk']
        params = kwargs
        if request.method == "GET":
            # queryset = Contributors.objects.all()
            # queryset = Contributors.objects.filter(project=params['pk'])
            # projets = get_object_or_404(queryset, project=params['pk'])
            try:
                queryset = Contributors.objects.filter(project=params['pk'])
            except Contributors.DoesNotExist:
                raise Http404("Aucun projet sous cet ID n'a de contributeur.")

            serializer = ContributorsSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        if request.method == "POST":
            contributor_data = request.data
            contributor_project = Projects.objects.get(pk=params['pk'])
            contributor_user = Users.objects.get(pk=contributor_data["user"])
            new_contributor = Contributors.objects.create(project=contributor_project,
                                                          user=contributor_user,
                                                          role=contributor_data["role"])
            new_contributor.save()
            serializer = ContributorsSerializer(new_contributor)
            return Response(serializer.data, status=200)

    # DELETE: /project/{id}/users/{id}/
    @action(detail=True, methods=['delete'], url_path='users/(?P<user_id>\d+)')
    def remove_user_from_project(self, request, user_id, pk=None, *args, **kwargs):
        # découpage de l'url récupéré, au niveau des / (/api/projects/4/users/3/)
        # pour récupérer le numéro du projet
        url_elements = request.get_full_path().split('/')
        project_number = url_elements[3]
        # récupération des contributions liées au projet et à l'user (auteur et contributeur)
        contribution_concerned = Contributors.objects.filter(project=project_number).filter(user=user_id)
        for contribution in contribution_concerned:
            contribution.delete()

        return Response({"message": "L'utilisateur a bien été supprimé de ce projet."}, status=200)

    #-----------ISSUES---------------

    # GET: /project/{id}/issues/
    @action(detail=True, methods=['get', 'post'])
    def issues(self, request, *args, **kwargs):
        """Création d'un path /projects/<id>/issues pour afficher les problèmes d'un projet,
        et en enregistrer de nouveaux """
        # récupération de <id> du projet dans /projects/<id>/issues via params['pk']
        params = kwargs
        if request.method == "GET":
            try:
                queryset = Issues.objects.filter(project=params['pk'])
            except Issues.DoesNotExist:
                raise Http404("Aucun problème pour ce projet.")

            serializer = IssuesSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        if request.method == "POST":
            issue_data = request.data
            issue_project = Projects.objects.get(pk=params['pk'])
            author_issue_user = Users.objects.get(pk=issue_data["author_user"])
            assignee_issue_user = Users.objects.get(pk=issue_data["assignee_user"])
            new_issue = Issues.objects.create(title=issue_data["title"], desc=issue_data["desc"],
                                              tag=issue_data["tag"],
                                              priority=issue_data["priority"],
                                              project=issue_project, status=issue_data["status"],
                                              author_user=author_issue_user,
                                              assignee_user=assignee_issue_user
                                              )
            new_issue.save()
            serializer = IssuesSerializer(new_issue)
            return Response(serializer.data, status=200)

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

