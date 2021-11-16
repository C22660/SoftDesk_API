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

    # GET: /projects/<id>/users
    # sources : https://stackoverflow.com/questions/67927493/djangorestframework-create-separate-urls-for-separate-functions-of-modelviewse
    @action(detail=True, methods=['get', 'post'])
    def users(self, request,  *args, **kwargs):
        """Création d'un path /projects/<id>/users pour afficher les contributeurs sur un projet,
        et enregistrer de nouveaux contributors"""
        # récupération de <id> dans /projects/<id>/users via params['pk']
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
            print(serializer.data)
            return Response(serializer.data)

        if request.method == "POST":
            contributor_data = request.data
            contributor_project = Projects.objects.get(pk=params['pk'])
            contributor_user = Users.objects.get(pk=params['pk'])
            new_contributor = Contributors.objects.create(project=contributor_project,
                                                          user=contributor_user,
                                                          role=contributor_data["role"])
            new_contributor.save()
            serializer = ContributorsSerializer(new_contributor)
            return Response(serializer.data)


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
